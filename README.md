# Recipe2LaTeX

Recipe2LaTeX is a simple repo to fetch recipes from websites such as [Chefkoch.de](https://www.chefkoch.de/) or [Marmiton.org](https://www.marmiton.org/). It is designed to create .tex files used together with the ["xcookybooky"](https://github.com/SvenHarder/xcookybooky) LaTeX package.

## Dependencies

```
urllib, json, sys, bs4, re

```

## Installation

```bash
pip3 install -r requirements.txt
```


## Usage

```python

python3 chefkoch2latex.py <url-to-recipe>
python3 marmiton2latex.py <url-to-recipe>
```
