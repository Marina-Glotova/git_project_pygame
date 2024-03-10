# Стратегическая игра «Битва за цвет»

## Описание игры

Игра «Битва за цвет» разработана по мотивам известной компьютерной игры Filler (https://ru.wikipedia.org/wiki/Filler). Для западного рынка игра выходила под названием 7 Colors.

В игру играют два игрока. В связи с неактуальностью в 2024 году игры двух людей на одном компьютере, игра реализована как игра человека с компьютером. 

Игра проходит на поле, состоящем из квадратных клеток нескольких разных цветов. В начале игры клетки раскрашены случайным образом. Каждый игрок начинает игру со своей стартовой клетки, находящейся на краю поля (в углу). Человек начинает с левого верхнего угла, компьютер - с правого нижнего. На каждом ходу игрок изменяет цвет стартовой клетки на любой другой — при этом все клетки, примыкающие к стартовой по стороне и окрашенные в тот же цвет, также перекрашиваются в выбранный цвет. Таким образом игрок «захватывает» соседние клетки, перекрашивая свою область в цвет этих клеток. Игрок не может выбрать цвет, которым на этом ходу окрашена его область или область противника.
Цель игры состоит в захвате более половины клеток игрового поля.
Размеры игрового поля - нечетные числа, поэтому  игра не может завершиться ничьей.

## Основные возможности программы

- Управление выбором цвета как мышью, так и клавишами вправо-влево. 
- Для выбора используется щелчок мышью на палитре, а также  клавиши пробел или энтер.
- Недоступные на очередном ходу цвета демонстрируются как цветные минусы.
- Перекрашивание цвета демонстрируется за счет изменения прозрачности области.
- Игра включает в себя 10 уровней. Чем больше уровень, тем больше клеток на поле, также увеличивается количество цветов с 5 до 8.
- После 10 уровня игра продолжается без усложнения, пока игрок не потерпит поражение.
- Компьютер может как выбирать свой ход случайно, так и выбирать самый лучший ход по количеству захваченных клеток.
- Чем выше уровень, тем меньше вероятность случайного выбора хода, то есть игра компьютера усиливается.
- Расчет игровой стратегии является NP-трудной задачей (https://arxiv.org/abs/1001.4420) поэтому возможно усиление игры компьютера только за счет расчета на несколько ходов вперед, но в таком случае задача игрока становится слишком сложной.
- В игре считается как текущее количество захваченных клеток для игрока и компьютера, так и количество очков, набранное игроком.
- Итогоое количество очков равно взвешенной сумме очков во всех пройденных раундах до поражения.
- После окончания игры выводится таблица рекордов, игроку предлагается ввести свое имя, результат добавляется в таблицу.
- Сохраняется 10 самых лучших результатов в файле records.csv.
- Если файл с рекордами отсутствует, он будет автоматически создан.
- Во время игры звучит музыкальное сопровождение - "Неаполитанская песенка" П.И. Чайковского.
- Программа пытается обрабатывать ошибки 

## Технические требования 
- Должна быть установлена библиотека pygame >= 2.0 
- В папке с программой должна быть папка data, в которой сохранены 
    - файл со шрифтом freesansbold.ttf,
    - картинки игрока и компьютера human.png, robot.png,
    - файл с мелодией pesenka.mid.