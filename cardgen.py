import json
import argparse
import os
import re
import textwrap
from PIL import Image, ImageDraw, ImageFont

def clean_disc_string(string):
    # replace <br> with line break
    cleaned_string = re.sub('<br>', '\n', string)

    return cleaned_string

def wrap_text(text, width):
    wrapped_text = '\n'.join(['\n'.join(textwrap.wrap(line, width,
                 break_long_words=False, replace_whitespace=False))
                 for line in text.splitlines() if line.strip() != ''])
    return wrapped_text

def scale_font_size(font, text, textbox_size):
    fontsize = 1

    W, H = textbox_size

    while(font.getsize(text)[0] < W and font.getsize(text)[1] < H):
        fontsize += 1
        font = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', fontsize)

    return fontsize

def print_card_name(art_frame, card_name, card_type, adjust_for_card_frame):
    font = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', 1)
    font_size = scale_font_size(font, card_name, (200,30))
    font = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', font_size)

    name = ImageDraw.Draw(art_frame)
    w, h = name.textsize(card_name, font=font)

    x_pos = art_frame.width//2 - w//2
    y_offset = 0
    if card_type == 1:
        y_pos = 48
    elif card_type == 2 or card_type == 3:
        if adjust_for_card_frame:
            y_offset = 5
        y_pos = 38
    else:
        if adjust_for_card_frame:
            y_offset = -10
        y_pos = 36

    x_offset = 10 if x_pos > 90 else 20

    name.text((x_pos + x_offset, y_pos + y_offset), card_name, fill='white', font=font)

def print_card_cost(art_frame, cost, card_type):
    card_cost = str(cost)
    font = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', 1)
    font_size = scale_font_size(font, card_cost, (60,60))
    font = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', font_size)

    cost = ImageDraw.Draw(art_frame)
    w, h = cost.textsize(card_cost, font=font)

    x_pos = 15
    if card_type == 1:
        y_pos = 25
    elif card_type == 2 or card_type == 3:
        y_pos = 25
    else:
        y_pos = 5

    x_offset = 0 if w > 40 else 10

    cost.text((x_pos + x_offset, y_pos), card_cost, fill='white', font=font)

def print_card_stats(art_frame, card_atk, card_hp, atk_xy, hp_xy, font_size):
    atk = str(card_atk)
    hp = str(card_hp)
    font = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', font_size)

    atk_img = ImageDraw.Draw(art_frame)
    hp_img = ImageDraw.Draw(art_frame)

    atk_img.text(atk_xy, atk, fill='white', font=font)
    hp_img.text(hp_xy, hp, fill='white', font=font)

def paste_craft_gem(canvas, craft, card_type):
    craft_list = ['neutral', 'forest', 'sword', 'rune', 'dragon', 'shadow', 'blood', 'haven', 'portal']

    icon = Image.open('templates/cards/craft_gems/'+craft_list[craft]+'.png')

    if card_type == 1:
        w = 167
        h = canvas.height - 57
    elif card_type == 2 or card_type == 3:
        w = 165
        h = canvas.height - 32
    else:
        w = 165
        h = canvas.height - 32

    canvas.paste(icon, (w, h), icon)

def paste_card_art(canvas, img_src, card_type):
    if card_type == 1:
        w = 257
        h = 327
        x = 48
        y = 86
        mask = Image.open("templates/cards/followers/follower_mask.png").convert('L').resize((w,h))
    elif card_type == 2 or card_type == 3:
        w = 257
        h = 324
        x = 48
        y = 82
        mask = Image.open("templates/cards/amulets/amulet_mask.png").convert('L').resize((w,h))
    else:
        w = 254
        h = 311
        x = 48
        y = 69
        mask = Image.open("templates/cards/spells/spell_mask.png").convert('L').resize((w,h))

    img = Image.open(img_src).resize((w,h))

    canvas.paste(img, (x,y), mask)

def paste_card_art_no_frame(card, art_canvas, card_details):
    card_type = card_details['char_type']
    if card_type == 1:
        size = (347,461)
    elif card_type == 2 or card_type == 3:
        size = (322, 423)
    else:
        size = (322, 405)

    art = Image.open(card_details['base_img']).resize(size)

    print_card_name(art, card_details['card_name'], 
                    card_details['char_type'], False)

    art_canvas.paste(art, (0,0), art)

    card.paste(art_canvas, (100, card.height//2 - art_canvas.height//2), art_canvas)

def paste_card_art_canvas(card, art_canvas, card_details):
    if "include_card_frame" in card_details and card_details['include_card_frame'] is False:
        paste_card_art_no_frame(card, art_canvas, card_details)
        return

    rarity_list = ['', 'bronze', 'silver', 'gold', 'lego']
    type_list = ['', 'follower', 'amulet', 'amulet', 'spell']

    card_rarity = rarity_list[card_details['rarity']]
    card_type = type_list[card_details['char_type']]
    art_frame = Image.open('templates/cards/'+card_type+'s/'+card_type+'_'+card_rarity+'.png')

    print_card_name(art_frame, card_details['card_name'], 
                    card_details['char_type'], True)
    print_card_cost(art_frame, card_details['cost'], card_details['char_type'])

    atk_xy = (30, 380)
    hp_xy = (295, 380)
    font_size = 60
    if card_details['char_type'] == 1:
        print_card_stats(art_frame, card_details['atk'], card_details['life'], atk_xy, hp_xy, font_size)

    if "base_img" not in card_details:
        card_details['base_img'] = "templates/cards/placeholder.png"
    paste_card_art(art_canvas, card_details['base_img'], card_details['char_type'])

    paste_craft_gem(art_frame, card_details['clan'], card_details['char_type'])

    art_canvas.paste(art_frame, (0,0), art_frame)

    card.paste(art_canvas, (100, card.height//2 - art_canvas.height//2), art_canvas)

def paste_card_text_canvas(card, text_canvas, art_canvas_size, card_details):
    text_font = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', 20)
    ct_canvas = Image.new('RGBA', (650, 600), color=(0,0,0,0))

    if card_details['char_type'] == 1:
        ct_xy = (0, 0)
        line_size = 6
    elif card_details['char_type'] == 2 or card_details['char_type'] == 3:
        ct_xy = (0, 30)
        line_size = 15
    else:
        ct_xy = (0, 30)
        line_size = 15

    line_width = 67

    card_text = wrap_text(clean_disc_string(card_details['skill_disc']), line_width)
    base_ct_img = ImageDraw.Draw(ct_canvas)
    base_ct_img.text(ct_xy, card_text, fill='white', font=text_font, spacing=line_size)

    ct_num_lines = len(card_text.splitlines())
    if ct_num_lines < 6:
        CT_TEXTBOX_TEMPLATE = 1
    elif ct_num_lines < 8:
        CT_TEXTBOX_TEMPLATE = 2
    else:
        CT_TEXTBOX_TEMPLATE = 3

    if card_details['char_type'] == 1:
        if CT_TEXTBOX_TEMPLATE == 1:
            text_frame = Image.open('templates/layout/follower_textbox_5_lines.png')
            base_atk_xy = (510, 33)
            base_hp_xy = (600, 33)
            evo_atk_xy = (510, 240)
            evo_hp_xy = (600, 240)
            evo_ct_xy = (0,205)
            ct_canvas_xy = (30,75)
        elif CT_TEXTBOX_TEMPLATE == 2:
            text_frame = Image.open('templates/layout/follower_textbox_7_lines.png')
            base_atk_xy = (490, 30)
            base_hp_xy = (580, 30)
            evo_atk_xy = (490, 257)
            evo_hp_xy = (580, 257)
            evo_ct_xy = (0,230)
            ct_canvas_xy = (30,68)
        else:
            text_frame = Image.open('templates/layout/follower_textbox_12_lines.png')
            base_atk_xy = (515, 31)
            base_hp_xy = (605, 31)
            evo_atk_xy = (515, 390)
            evo_hp_xy = (605, 390)
            evo_ct_xy = (0,358)
            ct_canvas_xy = (30,70)
    elif card_details['char_type'] == 2 or card_details['char_type'] == 3:
        text_frame = Image.open('templates/layout/amulet_textbox_9_lines.png')
        ct_canvas_xy = (30,70)
    else:
        text_frame = Image.open('templates/layout/spell_textbox_6_lines.png')
        ct_canvas_xy = (30,70)

    if card_details['char_type'] == 1:
        evo_card_text = wrap_text(clean_disc_string(card_details['evo_skill_disc']), line_width)
        evo_ct_img = ImageDraw.Draw(ct_canvas)
        evo_ct_img.text(evo_ct_xy, evo_card_text, fill='white', font=text_font, spacing=line_size)

        font_size = 32
        print_card_stats(text_frame, card_details['atk'], card_details['life'], base_atk_xy, base_hp_xy, font_size)
        print_card_stats(text_frame, card_details['evo_atk'], card_details['evo_life'], evo_atk_xy, evo_hp_xy, font_size)

    draw_box = ImageDraw.Draw(text_canvas)

    if card_details['char_type'] == 1:
        if CT_TEXTBOX_TEMPLATE == 1:
            draw_box.rectangle(((0,5),(670,460)), fill=(0,0,0,200))
        elif CT_TEXTBOX_TEMPLATE == 2:
            draw_box.rectangle(((0,5),(640,440)), fill=(0,0,0,200))
        else:
            draw_box.rectangle(((0,5),(670,540)), fill=(0,0,0,200))
    else:
        draw_box.rectangle(((0,5),(670,460)), fill=(0,0,0,200))

    text_canvas.paste(text_frame, (0,0), text_frame)
    text_canvas.paste(ct_canvas, ct_canvas_xy, ct_canvas)

    ac_w, ac_h = art_canvas_size
    card.paste(text_canvas, (ac_w + 120, card.height//2 - ac_h//2), text_canvas)

def paste_craft_icon(canvas, craft, pos):
    craft_list = ['neutral', 'forest', 'sword', 'rune', 'dragon', 'shadow', 'blood', 'haven', 'portal']

    icon = Image.open('templates/cards/craft_icons/'+craft_list[craft]+'.png')

    canvas.paste(icon, (pos[0],pos[1]), icon)

def paste_header_canvas(card, header_canvas, card_details):
    craft_list = ['Neutral', 'Forestcraft', 'Swordcraft', 'Runecraft',
                  'Dragoncraft', 'Shadowcraft', 'Bloodcraft', 'Havencraft', 'Portalcraft']

    craft = craft_list[card_details['clan']]

    font_1 = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', 36)
    font_2 = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', 22)

    h_height = header_canvas.height

    name = ImageDraw.Draw(header_canvas)
    name.text((50, h_height - h_height//2), card_details['card_name'], fill='white', font=font_1)

    text_width = 400
    text_height = 100
    info_text_canvas = Image.new('RGBA', (text_width, text_height), color=(0,0,0,0))
    craft_label = ImageDraw.Draw(info_text_canvas)
    trait_label = ImageDraw.Draw(info_text_canvas)

    craft_label.text((0,0), 'Class:', fill='white', font=font_2)
    if card_details['clan'] != 0:
        paste_craft_icon(info_text_canvas, card_details['clan'], (60, 0))
        craft_label.text((95, 0), craft, fill='white', font=font_2)
    else:
        craft_label.text((65, 0), craft, fill='white', font=font_2)

    trait_label.text((0, 30), 'Trait:', fill='white', font=font_2)
    trait_label.text((90, 30), card_details['tribe_name'], fill='white', font=font_2)

    header_canvas.paste(info_text_canvas, (card.width - text_width, h_height//4), info_text_canvas)

    divider = Image.open('templates/layout/header_divider.png')
    header_canvas.paste(divider, (0, h_height - 10), divider)

    card.paste(header_canvas, (100, 0), header_canvas)

def get_default_background(craft):
    default_backgrounds = [
        "templates/backgrounds/background_Morning_Star.png",
        "templates/backgrounds/background_Forest.png",
        "templates/backgrounds/background_Castle.png",
        "templates/backgrounds/background_Laboratory.png",
        "templates/backgrounds/background_Mountains.png",
        "templates/backgrounds/background_Mansion.png",
        "templates/backgrounds/background_Darkstone.png",
        "templates/backgrounds/background_Hall.png",
        "templates/backgrounds/background_Track_Night.png"
    ]

    return default_backgrounds[craft]

def cardgen(card_json, out_dir):
    template_width = 1200
    template_height = 700

    header_width = 1200
    header_height = 100

    text_canvas_width = 680
    text_canvas_height = 600

    os.makedirs(out_dir, exist_ok=True)

    with open(card_json, "r") as data:
        cards = json.load(data)

    for i, card_details in enumerate(cards):
        if card_details['char_type'] == 1:
            art_canvas_width = 347
            art_canvas_height = 461
        elif card_details['char_type'] == 2 or card_details['char_type'] == 3:
            art_canvas_width = 322
            art_canvas_height = 423
        else:
            art_canvas_width = 322
            art_canvas_height = 405

        card = Image.new('RGBA', (template_width, template_height), color=(0,0,0,255))

        bg_src = card_details.get('background_img', get_default_background(card_details['clan']))

        background = Image.open(bg_src)
        background.putalpha(100)
        card.paste(background, None, background)

        header_canvas = Image.new('RGBA', (header_width, header_height), color=(0,0,0,0))
        art_canvas = Image.new('RGBA', (art_canvas_width, art_canvas_height), color=(0,0,0,0))
        text_canvas = Image.new('RGBA', (text_canvas_width, text_canvas_height), color=(0,0,0,0))

        paste_header_canvas(card, header_canvas, card_details)
        paste_card_art_canvas(card, art_canvas, card_details)
        paste_card_text_canvas(card, text_canvas, art_canvas.size, card_details)

        card.save(out_dir + "/card_" + str(i) + ".png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and generate custom SV cards.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file',
                         help="JSON file containing card input data")
    parser.add_argument('out_dir', nargs='?', default='cards/',
                         help="Directory where generated cards will be placed")

    args = parser.parse_args()

    cardgen(args.file, args.out_dir)
