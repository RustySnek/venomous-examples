defmodule VenomousExamplesTest do
  use ExUnit.Case
  doctest VenomousExamples

  test "greets the world" do
    assert VenomousExamples.hello() == :world
  end
end
