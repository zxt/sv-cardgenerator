# sv-cardgenerator

A custom card generator for Shadowverse

## Usage
```bash
python ./svcardgenerator/cardgen.py -h
```

```bash
usage: cardgen.py [-h] file [out_dir]

Process and generate custom SV cards.

positional arguments:
  file        JSON file containing card input data
  out_dir     Directory where generated cards will be placed (default: cards/)

optional arguments:
  -h, --help  show this help message and exit
```
## Card Data Format

The file you pass into the program should be a JSON file of the following format:

```json
[
    {
        "card_name": ,
        "char_type": ,
        "clan": ,
        "tribe_name": ,
        "skill_disc": ,
        "evo_skill_disc": ,
        "cost": ,
        "atk": ,
        "life": ,
        "evo_atk": ,
        "evo_life": ,
        "rarity": ,
        "base_img": ,
        "background_img": ,
        "include_card_frame": 
    },
    ...
]
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `card_name` | `string` | Name of the card |
| `char_type` | `int` | Type of the card. <br>1 = Follower <br>2 = Amulet <br>3 = Countdown Amulet <br>4 = Spell |
| `clan` | `int` | Craft/class of the card. <br>0 = Neutral <br> 1 to 8 = Forest to Portal, following ingame order |
| `tribe_name` | `string` | Trait of the card, e.g. 'Commander', 'Natura', etc. |
| `skill_disc` | `string` | Base card text |
| `evo_skill_disc` | `string` | Evolved card text |
| `cost` | `int` | pp cost of the card |
| `atk` | `int` | Attack value of the card |
| `life` | `int` | Defense value of the card |
| `evo_atk` | `int` | Evolved Attack value of the card |
| `evo_life` | `int` | Evolved Defense value of the card |
| `rarity` | `int` | Rarity of the card. <br>1 = Bronze <br>2 = Silver <br>3 = Gold <br>4 = Legendary |
| `base_img` | `string` | Path to an image to use as the card art |
| `background_img` | `string` | Path to an image to use as the background image (*optional*) |
| `include_card_frame` | `boolean` | Whether to include a card frame in the output (default: True) |


  
## Built With

* python
* [Pillow](https://pillow.readthedocs.io/en/stable/)

  
## License

[MIT](https://github.com/zxt/sv-cardgenerator/blob/master/LICENSE)