# Курсовой проект по ТИМП

##1. Задача
Разработать программу, способную распознавать печатную строку нот в скрипичном ключе с изображения
 в формате `*.png/*.jpg` и интерпретировать в мелодию в формате `*.mid`. Программа должна распознавать:
 - ноты, высотой: от соль малой октавы до ми третьей октавы;
 - следующие длительности: целая, половинная, четвертная, восьмая, шестнадцатая и все, кроме шестнадцатых, с точкой;
 - паузы: целая, половинная, четвертная, восьмая;
 - диезы и бемоли при ключе.
 
##2. Описание
Программе подаются на вход два аргумента: `--file` - обязательный, `--output` - опциональный.
 `--file` задает путь до распознаваемого `*.png/*.jpg` изображения, `--output` - путь до выходного `*.mid` - файла.
 По умолчанию мелодия записывается в файл `output.mid` в текущем каталоге.
 
##3. Установка
1. Скачать архив, соответствующий операционной системе.
2. Распаковать его в необходимую папку.
3. Перейти в папку, куда был распакован архив.
4. Переместить содержимое папки `dist/` на один каталог вверх.
 
##4. Пример использования программы
Примеры распознаваемых последовательностей находятся в папке `samples/`.
```
$ ./note-interpreter --file samples/picture_1.png
```
```
$ ./note-interpreter --file samples/picture_1.png --output melody.mid
```
##5. architecture (e.g. mermaid)
##6. Отчет по работе нейросети
```
Total notes: 833. Percent of right evaluations 93.75750300120048%
Total Whole: 49. Percent of right evaluations 100.0%
Total Dotted Whole: 5. Percent of right evaluations 0.0%
Total Half: 128. Percent of right evaluations 94.53125%
Total Dotted Half: 18. Percent of right evaluations 66.66666666666667%
Total Quarter: 206. Percent of right evaluations 97.0873786407767%
Total Dotted Quarter: 20. Percent of right evaluations 80.0%
Total Eighth: 275. Percent of right evaluations 93.45454545454545%
Total Dotted Eighth: 10. Percent of right evaluations 50.0%
Total 16th: 122. Percent of right evaluations 99.18032786885246%
```
##6. links (demo, examples, building, testing)
##7. TODO
- Обработка диезов, бемолей и бекаров не только при ключе;
- Распознавание нот в басовом ключе;
- Обработка аккордов.

## Выполнили
Бояркина Елизавета, студент группы ИУ8-31 @freesummerwind 

Кидинова Дарья, студент группы ИУ8-31 @ezuryy
