from urllib.parse import parse_qs


def test_parse_qs():
    my_values = parse_qs('red=5&blue=0&green=', keep_blank_values=True)
    print(repr(my_values))

    print('Red:     ', my_values.get('red'))
    print('Green:   ', my_values.get('green'))
    print('Opacity: ', my_values.get('opacity'))

def test_zip():
    years = {2019, 2020, 2021, 2022}
    months = {'Jan', 'Feb', 'Mar', 'Apr', 'May'}
    days = {1, 2, 3, 4, 5, 6}

    for year, month, day in zip(years, months, days):
        print(f'Today is: {year}-{month}-{day}')


if __name__ == '__main__':
    # test_parse_qs()
    test_zip()