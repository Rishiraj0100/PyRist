# PyRist
The programming language made by me ([@Rishiraj0100](https://GitHub.com/Rishiraj0100))

## Usage

First of all, it should be installed by
```sh
python3 -m pip install git+https://github.com/Rishiraj0100/PyRist/
```

Create a file named `main.rist`<br />
A sample code is given here
```rist
@+ os, pprint;
+@ typing @+ Union;

define cls{}:;
  os.system{"cls" if os.name == "nt" else "clear"};

cls{};

define something{arg: Union[str, int]}:;
  pprint.pprint{["myText", [arg]]};

something{"text2"};
```

Then in your shell
```sh
python3 -m ristpy main.rist
```

If you want to compile it to python then in your python file
```py
from ristpy import rist, execute

print(rist("main.rist"))
# if you want some text then

code = """
print{"hello"};
"""
print(rist(code, fp=False))
# if you wanna execute then
execute(rist(code, fp=False))
execute(rist('main.rist'))
```

## Syntax
### Note
Every line should end with `;` only if line is not empty
### Importing
#### What can it Import?

It can Import all python3 modules

#### How to Import?
In python you do `import asyncio`

In rist you have to do `@+ asyncio;`

In python you do `from aiohttp import web`

In rist you have to do `+@ aiohttp @+ web;`

### More Syntax

Coming soon....
