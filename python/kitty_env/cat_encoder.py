from dataclasses import dataclass

from erlport.erlang import set_decoder, set_encoder
from erlport.erlterms import Atom, Map


@dataclass
class Cat:
    name: str
    color: str
    favorite_snacks: list[str]


def handle_types():
    set_encoder(encoder)
    set_decoder(decoder)
    return Atom("ok".encode("utf-8"))


# By default erlport converts regular strings into charlists.
# We can handle most of the cases by encoding strings into utf-8 with a simple function like this.
def encode_basic_type_strings(data):
    if isinstance(data, str):
        return data.encode("utf-8")
    elif isinstance(data, list):
        return [encode_basic_type_strings(item) for item in data]
    elif isinstance(data, tuple):
        return tuple(encode_basic_type_strings(item) for item in data)
    elif isinstance(data, dict):
        return {key: encode_basic_type_strings(value) for key, value in data.items()}
    else:
        return data


def encoder(value: any):
    if isinstance(value, Cat):
        # We .__dict__ the class and normalize it's key,values.
        # Erlport will convert this dict into a Map
        return {
            Atom(
                encode_basic_type_strings(key)
            ): encode_basic_type_strings(  # Convert the keys to atoms
                val
            )  # utf-8 Encode strings inside
            for key, val in value.__dict__.items()
        }
    # If none matches just encode strings and return value
    return encode_basic_type_strings(value)


def decoder(value: any):
    # Elixir strings convert to bytes, we can decode them into utf-8 strings.
    if isinstance(value, bytes):
        return value.decode("utf-8")
    if isinstance(value, Map):
        # If its a Map custom type we decode bytes into utf-8 strings
        return {
            key.decode("utf-8"): [v.decode("utf-8") for v in val]
            for key, val in value.items()
        }
    # if none get caught we just return the raw inputs
    return value
