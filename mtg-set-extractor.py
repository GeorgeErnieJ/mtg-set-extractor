import json

def open_data(dataname):

    with open(dataname, encoding='utf-8') as f:
        data = json.load(f)

    f.close()

    return(data)


def set_filter(data, setname):

    filtered_list = []

    for card in data:

        if card['set'] == setname:

            filtered_list.append(card)

    return(filtered_list)

def output_cards(data, filename='output'):

    filename += '.txt'

    output_file = open(filename, 'w+')

    try:

        for card in data:

            string = card["name"] + '\n'
            output_file.write(string)

    except:
        print('there was an error')
        pass

    output_file.close()



setname = 'mh2'


data = open_data('oracle-cards.json')

filtered_data = set_filter(data, setname)

output_cards(filtered_data, setname)