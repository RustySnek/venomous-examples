# VenomousExamples

## Loading modules
Python will look for *.py and __init__.py files under subdirectories of the module_path

For unnamed processes
```elixir
import Config

config :venomous, :snake_manager, %{
    python_opts: [
        # Default scope is project directory
        module_paths: ["python/"]
    ]
}
```
Named processes have their own separate configuration
```elixir
import Venomous

adopt_snake_pet(:kitty, module_paths: ["python/"])
```

## Examples 
Setup a python venv inside python/ and install requests
```
python -m venv python/venv
source python/venv/bin/activate
pip install requests
deactivate
```
Now inside `:module_paths` config, set our modules paths
This will include all venv packages and the files we put inside python/ dir
```elixir
config :venomous, :snake_manager, %{
    python_opts: [
        # Default scope is project directory
        module_paths: ["python/", "python/venv/lib/{PYTHON_VERSION}/site-packages/"]
    ]
}
```
Now lets run our example app and try things out
```bash
iex -S mix run

# Try running the included factorial() func inside my_module.py
iex(5)> Venomous.SnakeArgs.from_params(:my_module, :factorial, [5]) |> Venomous.python()
120

# Lets try using the installed requests library
iex(3)> Venomous.SnakeArgs.from_params(:client, :request_server, ["http://example.com"]) |> Venomous.python()
"<!doctype html>\n<html>\n<head>\n    <title>Example Domain</title>\n\n    <meta charset=\"utf-8\" />\n    <meta http-equiv=\"Content-type\" content=\"text/html; charset=utf-8\" />\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n    <style type=\"text/css\">\n    body {\n        background-color: #f0f0f2;\n        margin: 0;\n        padding: 0;\n        font-family: -apple-system, system-ui, BlinkMacSystemFont, \"Segoe UI\", \"Open Sans\", \"Helvetica Neue\", Helvetica, Arial, sans-serif;\n        \n    }\n    div {\n        width: 600px;\n        margin: 5em auto;\n        padding: 2em;\n        background-color: #fdfdff;\n        border-radius: 0.5em;\n        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);\n    }\n    a:link, a:visited {\n        color: #38488f;\n        text-decoration: none;\n    }\n    @media (max-width: 700px) {\n        div {\n            margin: 0 auto;\n            width: auto;\n        }\n    }\n    </style>    \n</head>\n\n<body>\n<div>\n    <h1>Example Domain</h1>\n    <p>This domain is for use in illustrative examples in documents. You may use this\n    domain in literature without prior coordination or asking for permission.</p>\n    <p><a href=\"https://www.iana.org/domains/example\">More information...</a></p>\n</div>\n</body>\n</html>\n"

# Now lets get into named processes
iex(14)> Venomous.adopt_snake_pet(:kitty, module_paths: "python/kitty_env")
{:ok, :kitty}
# This created a python process named :kitty with access to the "python/kitty_env" modules
# Because the kitty_env directory does not contain __init__.py snake_manager processes won't see the modules inside

iex(15)> meow = Venomous.SnakeArgs.from_params(:only_cat_module, :meow, [2])
%Venomous.SnakeArgs{module: :only_cat_module, func: :meow, args: [2]}
iex(16)> Venomous.pet_snake_run(meow, :kitty)
~c"Meow!Meow!"
# Notice that we've got a charlist instead of a string
# This is because we haven't included the encoder function for
# the :kitty process like we did for snake_manager ones inside config.exs.

# So let's kill our kitty process and re-declare its settings
iex(17)> Venomous.slay_pet_worker(:kitty)
:ok
iex(18)> Venomous.adopt_snake_pet(:kitty, module_paths: "python/kitty_env", erlport_encoder: %{module: :cat_encoder, func: :handle_types, args: []})
{:ok, :kitty}
iex(19)> Venomous.pet_snake_run(meow, :kitty)
"Meow!Meow!"
```

## Concurrent processes
Venomous handles all concurrent processes inside snake manager
```bash
iex(21)> sleep = Venomous.SnakeArgs.from_params(:time, :sleep, [0.5])                                                                 
%Venomous.SnakeArgs{
  module: :time,
  func: :sleep,
  args: [0.5]
}
iex(22)> sweet_dreams = 1..1000 |> Enum.map(fn _ -> Task.async(fn -> Venomous.python!(sum_args) end)end) |> Task.await_many()
# This should take less than 5 seconds with 50 max_children
# Now we can list all of the spawned and ready processes
iex(24)> Venomous.list_alive_snakes
[
  {#PID<0.17735.1>, #PID<0.17736.1>, 43498, :ready,
   ~U[2024-06-16 12:43:19.387564Z]},
  {#PID<0.17737.1>, #PID<0.17741.1>, 43500, :ready,
   ~U[2024-06-16 12:43:19.387569Z]},
  {#PID<0.17822.1>, #PID<0.17826.1>, 43534, :ready,
   ~U[2024-06-16 12:43:19.387595Z]},
   ...
]
# If we leave these untouched they will be cleaned up in about 10min as is declared in config.exs
```

