Для работы удобно использовать PyCharm

Запустите PyCharm. Создайте новый проект. Скопируйте все файлы из папки "dist"
Установите все пакеты из requirements.txt

Дождитесь завершения индексации!

Теперь можно запустить проект. Запускаем main.py

Вначале откроется начальный экран, состоящий из 3 кнопок:
    start - начать игру
    settings - настойки
    exit - выйти из игры и завершить работу программы

Проект представляет собой игру-лабиринт на двоих игроков.
Задача: выйти из лабиринта.
Чтобы выйти из лабиринта нужно пройти 3 карты. 
Чтобы перейдти на следующую карту нужно найти ключ и принести его к двери.
УПРАВЛЕНИЕ:
    1 игрок:
        W - движение вверх
        A - движение влево
        S - движение вниз
        D - движение вправо
        E - взаимодействие
    2 игрок:
        Up arrow - движение вверх
        Left arrow - движение влево
        Down arrow - движение вниз
        Right arrow - движение вправо
        / - взаимодействие
    Общие:
        Esc - пауза (В паузе можно выйти на начальный экран или продолжить игру)

Чтобы поднять ключ или пройти в дверь нужно нажать клавишу взаимодействия определенного игрока.
На последнем (3) уровне не нужно нажимать клавиши в дверях, чтобы пройти игру.
Требуется, чтобы оба игрока одновременно находились в дверях с ключами

При проходении 3 уровня появляется финальный экран.
На финальном экране: счет, лучший счет,
    кнопка для выхода на стартовый экран и кнопка выхода из игры и завершения прграммы

Интерфейс дружественный, все интуитивно понятно
