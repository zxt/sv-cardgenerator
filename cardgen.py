from PIL import Image, ImageDraw, ImageFont

def scale_font_size(font, text, textbox_size):
    fontsize = 1

    W, H = textbox_size

    while(font.getsize(text)[0] < W and font.getsize(text)[1] < H):
        fontsize += 1
        font = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', fontsize)

    return fontsize

def print_card_name(art_frame, card_name, card_type):
    font = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', 1)
    font_size = scale_font_size(font, card_name, (200,30))
    font = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', font_size)

    name = ImageDraw.Draw(art_frame)
    w, h = name.textsize(card_name, font=font)

    x_pos = art_frame.width//2 - w//2
    if card_type == 1:
        y_pos = 48
    elif card_type == 2 or card_type == 3:
        y_pos = 48
    else:
        y_pos = 26

    x_offset = 0 if x_pos > 80 else 20

    name.text((x_pos + x_offset, y_pos), card_name, fill='white', font=font)

def print_card_cost(art_frame, card_cost, card_type):
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
    font = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', font_size)

    atk = ImageDraw.Draw(art_frame)
    hp = ImageDraw.Draw(art_frame)

    atk.text(atk_xy, card_atk, fill='white', font=font)
    hp.text(hp_xy, card_hp, fill='white', font=font)

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
        mask = Image.open('templates/cards/followers/follower_mask.png').convert('L').resize((w,h))
    else:
        mask = Image.open('templates/cards/spells/spell_mask.png').convert('L').resize((w,h))

    img = Image.open(img_src).resize((w,h))

    canvas.paste(img, (x,y), mask)

def paste_card_art_canvas(card, art_canvas, card_details):
    rarity_list = ['', 'bronze', 'silver', 'gold', 'lego']
    type_list = ['', 'follower', 'amulet', 'amulet', 'spell']

    card_rarity = rarity_list[card_details['rarity']]
    card_type = type_list[card_details['card_type']]
    art_frame = Image.open('templates/cards/'+card_type+'s/'+card_type+'_'+card_rarity+'.png')

    print_card_name(art_frame, card_details['card_name'], card_details['card_type'])
    print_card_cost(art_frame, card_details['card_cost'], card_details['card_type'])

    atk_xy = (30, 380)
    hp_xy = (295, 380)
    font_size = 60
    if card_details['card_type'] == 1:
        print_card_stats(art_frame, card_details['card_atk'], card_details['card_hp'], atk_xy, hp_xy, font_size)

    paste_craft_gem(art_frame, card_details['craft'], card_details['card_type'])

    paste_card_art(art_frame, card_details['base_img'], card_details['card_type'])

    art_canvas.paste(art_frame, (0,0), art_frame)

    card.paste(art_canvas, (0, template_height//2 - art_canvas.height//2), art_canvas)

def paste_card_text_canvas(card, text_canvas, card_details):
    text_frame = Image.open('templates/layout/textbox.png')

    base_atk_xy = (500, 50)
    base_hp_xy = (590, 50)
    evo_atk_xy = (500, 245)
    evo_hp_xy = (590, 245)
    font_size = 32
    print_card_stats(text_frame, card_details['card_atk'], card_details['card_hp'], base_atk_xy, base_hp_xy, font_size)
    print_card_stats(text_frame, card_details['card_atk'], card_details['card_hp'], evo_atk_xy, evo_hp_xy, font_size)

    text_font = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', 20)
    ct_canvas = Image.new('RGBA', (650, 600), color=(0,0,0,0))
    base_card_text = ImageDraw.Draw(ct_canvas)
    base_card_text.multiline_text((0, 0), card_details['skill_disc'], fill='white', font=text_font, spacing=5)
    evo_card_text = ImageDraw.Draw(ct_canvas)
    evo_card_text.multiline_text((0,200), card_details['evo_skill_disc'], fill='white', font=text_font, spacing=5)

    text_canvas.paste(text_frame, (0,0), text_frame)
    text_canvas.paste(ct_canvas, (50,85), ct_canvas)

    card.paste(text_canvas, (art_canvas_width + 20, template_height//2 - art_canvas.height//2), text_canvas)

def paste_craft_icon(canvas, craft, pos):
    craft_list = ['neutral', 'forest', 'sword', 'rune', 'dragon', 'shadow', 'blood', 'haven', 'portal']

    icon = Image.open('templates/cards/craft_icons/'+craft_list[craft]+'.png')

    canvas.paste(icon, (pos[0],pos[1]), icon)

def paste_header_canvas(card, header_canvas, card_details):
    craft_list = ['Neutral', 'Forestcraft', 'Swordcraft', 'Runecraft',
                  'Dragoncraft', 'Shadowcraft', 'Bloodcraft', 'Havencraft', 'Portalcraft']

    craft = craft_list[card_details['craft']]

    font_1 = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', 36)
    font_2 = ImageFont.truetype('templates/fonts/Seagull-Medium.otf', 22)

    name = ImageDraw.Draw(header_canvas)
    name.text((50, header_height - header_height//2), card_details['card_name'], fill='white', font=font_1)

    text_width = 400
    text_height = 100
    info_text_canvas = Image.new('RGBA', (text_width, text_height), color='black')
    craft_label = ImageDraw.Draw(info_text_canvas)
    trait_label = ImageDraw.Draw(info_text_canvas)

    craft_label.text((0,0), 'Class:', fill='white', font=font_2)
    paste_craft_icon(info_text_canvas, card_details['craft'], (60, 0))
    craft_label.text((95,0), craft, fill='white', font=font_2)

    trait_label.text((0, 30), 'Trait: '+card_details['trait'], fill='white', font=font_2)

    header_canvas.paste(info_text_canvas, (template_width - text_width, header_height//4), info_text_canvas)

    divider = Image.open('templates/layout/header_divider.png')
    header_canvas.paste(divider, (0, header_height - 10), divider)

    card.paste(header_canvas, (0, 0), header_canvas)

template_width = 1200
template_height = 700

header_width = 1200
header_height = 100

text_canvas_width = 700
text_canvas_height = 700

card_details = {}
card_details['card_name'] = "Legendary Goblin"
card_details['craft'] = 5
card_details['trait'] = 'goblin'
card_details['card_type'] = 1
card_details['rarity'] = 4
card_details['card_cost'] = '1'
card_details['card_atk'] = '3'
card_details['card_hp'] = '3'
card_details['skill_disc'] = 'Storm.\nFanfare: Give another goblin +1 attack until the end of the turn.'
card_details['evo_skill_disc'] = 'Storm.'
card_details['base_img'] = 'goblin.jpeg'

if card_details['card_type'] == 1:
    art_canvas_width = 347
    art_canvas_height = 461
elif card_details['card_type'] == 2 or card_details['card_type'] == 3:
    art_canvas_width = 322
    art_canvas_height = 423
else:
    art_canvas_width = 322
    art_canvas_height = 405

card = Image.new('RGBA', (template_width, template_height), color='black')
header_canvas = Image.new('RGBA', (header_width, header_height), color='black')
art_canvas = Image.new('RGBA', (art_canvas_width, art_canvas_height), color='black')
text_canvas = Image.new('RGBA', (text_canvas_width, text_canvas_height), color='black')

paste_header_canvas(card, header_canvas, card_details)
paste_card_art_canvas(card, art_canvas, card_details)
paste_card_text_canvas(card, text_canvas, card_details)

card.save('card.png')
