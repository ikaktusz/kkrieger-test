# Тестовое задание

При выполнении задания был использован **PresentMon 1.8.0** для трассировки событий Windows(ETW)  
"msBetweenPresents" метрика использована для подсчёта среднего fps.

CheatEngine и части открытого кода для поиска текущего состояния игры.

https://github.com/GameTechDev/PresentMon  
https://github.com/farbrausch/fr_public/tree/master/werkkzeug3_kkrieger

## Использование
Поддерживается только Windows.  
Для запуска теста нужны права администратора.  

Конфигурация выведена в отдельный файл config.yaml

Перед началом убедитесь, что в директории скрипта находится исполняемый файл PresentMon-1.8.0.exe  
Ссылка на скачивание: https://github.com/GameTechDev/PresentMon/releases/tag/v1.8.0  
  
`git clone https://github.com/ikaktusz/kkrieger-test.git`  
`cd kkrieger-test`  
`pip install -r requirements.txt`  

`python3 main.py game_path -o output_path`

## Вывод скрипта
Все файлы сохраняются в директорию `-o output_path`:  
1) Лог работы скрипта  
2) Средний fps за сессию  
3) Лог записи PresentMon в формате csv  
4) Информация о производительности системы в формате csv  
5) Информация о системе в формате json  
6) Папка screenshots с сохранёнными скриншотами в начале/конце  

## P.S.
Ходьбу до препятствия реализовать не удалось:((  
Либо нужно n^2 времени:)  
Идея была в том, чтобы найти float x/y/z координаты игрока и если они не меняются n-времени регистрировать препятствие. (Первое, что пришло в голову)  

Ну и многие возможные ошибки не отловлены...  
