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


def test_sort():
    class Tool:
        def __init__(self, name, weight):
            self.name = name
            self.weight = weight

        def __repr__(self):
            return f'Tool({self.name!r}, {self.weight})'

    power_tools = [Tool('drill', 4), Tool('circular saw', 5), Tool('jackhammer', 40), Tool('sander', 4)]

    # 先按 weight 降序排序，再按 name 升序排序
    print('order by weight desc firstly, order by name asc finally')
    power_tools.sort(key=lambda x: x.name)
    print(power_tools)
    power_tools.sort(key=lambda x: x.weight, reverse=True)
    print(power_tools)

    # 先按 name 升序排序，再按 weight 降序排序
    print('order by name asc firstly, order by weight desc finally')
    power_tools.sort(key=lambda x: x.weight, reverse=True)
    print(power_tools)
    power_tools.sort(key=lambda x: x.name)
    print(power_tools)

    # 先按 weight 升序排序，再按 name 降序排序
    print('order by weight asc firstly, order by name desc finally')
    power_tools.sort(key=lambda x: x.name, reverse=True)
    print(power_tools)
    power_tools.sort(key=lambda x: x.weight)
    print(power_tools)

    # 先按 name 降序排序，再按 weight 升序排序
    print('order by name desc firstly, order by weight asc finally')
    power_tools.sort(key=lambda x: x.weight)
    print(power_tools)
    power_tools.sort(key=lambda x: x.name, reverse=True)
    print(power_tools)

if __name__ == '__main__':
    # test_parse_qs()
    # test_zip()
    test_sort()
