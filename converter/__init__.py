from typing import TypeVar, Generic

Input = TypeVar('Input')
Output = TypeVar('Output')
Mid = TypeVar('Mid')
NextOutput = TypeVar('NextOutput')

class RawConverter (Generic[Input, Output]):
  def convert (self, input: Input) -> Output:
    return input

class Converter (RawConverter[Input, Output]):
  def __or__ (self, next_converter: RawConverter[Output, NextOutput]):
    return CombinedConverter[Input, NextOutput, Output](self, next_converter)

class CombinedConverter (Converter[Input, Output], Generic[Input, Mid, Output]):
  def __init__ (self, input_side_converter: Converter[Input, Mid], output_side_converter: Converter[Mid, Output]):
    self.input_side_converter = input_side_converter
    self.output_side_converter = output_side_converter

  def convert (self, input: Input) -> Output:
    return self.output_side_converter.convert(self.input_side_converter.convert(input))
