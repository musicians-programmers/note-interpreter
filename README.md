# Курсовой проект по ТИМП

## 1.Задача
Разработать программу, способную распознавать печатную строку нот в скрипичном ключе с изображения
в формате `*.png/*.jpg` и интерпретировать в мелодию в формате `*.mid`. Программа должна распознавать:
 - ноты, высотой: от соль малой октавы до ми третьей октавы;
 - следующие длительности: целая, половинная, четвертная, восьмая, шестнадцатая и все, кроме шестнадцатых, с точкой;
 - паузы: целая, половинная, четвертная, восьмая;
 - диезы и бемоли при ключе.
 
## 2. Описание
Программе подаются на вход два аргумента: `--file` - обязательный, `--output` - опциональный.
 `--file` задает путь до распознаваемого `*.png/*.jpg` изображения, `--output` - путь до выходного `*.mid` - файла.
 По умолчанию мелодия записывается в файл `output.mid` в текущем каталоге.
 
## 3. Установка
1. Скачать архив, соответствующий операционной системе.
2. Распаковать его в необходимую папку.
3. Перейти в папку, куда был распакован архив.
4. Переместить содержимое папки `dist/` на один каталог вверх.
 
## 4. Пример использования программы
Примеры распознаваемых последовательностей находятся в папке `samples/`.
```
$ ./note-interpreter --file samples/picture_1.png
```
```
$ ./note-interpreter --file samples/picture_1.png --output melody.mid
```
## 5. Архитектура
[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVERcbkFb0J_QvtC00LHQvtGAINC80LDRgdGI0YLQsNCx0LAsINC_0L7QuNGB0Log0YjQsNCx0LvQvtC90L3Ri9GFINC40LfQvtCx0YDQsNC20LXQvdC40LldIC0tPiB80YHQv9C40YHQvtC6INCy0YHQtdGFINC90LDQudC00LXQvdC90YvRhSDQvdCwINC60LDRgNGC0LjQvdC60LUg0YHQuNC80LLQvtC70L7QsnwgQlvQntC_0YDQtdC0LiDQutC-0L7RgNC00LjQvdCw0YIg0L3QsNC50LTQtdC90L3Ri9GFINGB0LjQvNCy0L7Qu9C-0LIsINCy0YvQtNC10LvQtdC90LjQtSDQuNGFINC90LAg0LrQsNGA0YLQuNC90LrQtV1cbkIgLS0-IHzRgdC_0LjRgdC-0Log0YHQuNC80LLQvtC70L7QsiArINC60YDQsNGB0LjQstCw0Y8g0LrQsNGA0YLQuNC90LrQsHxDW9Ce0L_RgNC10LQuINCy0YvRgdC-0YLRgyDQvdC-0YIg0Lgg0LfQvdCw0LrQvtCyLCDQt9C90LDRjyDQutC-0L7RgNC00LjQvdCw0YLRiyDQuNGFINGG0LXQvdGC0YDQvtCyINC4INC90L7RgtC90L7Qs9C-INGB0YLQsNC90LBdXG5DIC0tPiB80LfQvdCw0LXQvCwg0LrQsNC60YPRjiDQstGL0YHQvtGC0YMg0L3Rg9C20L3QviDRgdGL0LPRgNCw0YLRjHwgRFvQntC_0YDQtdC0LiDQtNC70LjRgtC10LvRjNC90L7RgdGC0Ywg0L3QvtGC0Ysg0YEg0L_QvtC80L7RidGM0Y4g0L3QtdC50YDQvtC90L3QvtC5INGB0LXRgtC4XVxuRCAtLT4gfNC30L3QsNC10LwsINC60LDQutC40LUg0LTQu9C40YLQtdC70YzQvdC-0YHRgtC4INC90YPQttC90L4g0YHRi9Cz0YDQsNGC0Yx8IEVb0J_RgNC10L7QsdGA0LDQt9GD0LXQvCDQsiAqLm1pZCDQv9C-0LvRg9GH0LXQvdC90YvQuSDRgdC_0LjRgdC-0Log0YHQuNC80LLQvtC70L7QsiDQt9C90LDQutC4ICsg0L3QvtGC0YsgKyDQv9Cw0YPQt9GLXSIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggVERcbkFb0J_QvtC00LHQvtGAINC80LDRgdGI0YLQsNCx0LAsINC_0L7QuNGB0Log0YjQsNCx0LvQvtC90L3Ri9GFINC40LfQvtCx0YDQsNC20LXQvdC40LldIC0tPiB80YHQv9C40YHQvtC6INCy0YHQtdGFINC90LDQudC00LXQvdC90YvRhSDQvdCwINC60LDRgNGC0LjQvdC60LUg0YHQuNC80LLQvtC70L7QsnwgQlvQntC_0YDQtdC0LiDQutC-0L7RgNC00LjQvdCw0YIg0L3QsNC50LTQtdC90L3Ri9GFINGB0LjQvNCy0L7Qu9C-0LIsINCy0YvQtNC10LvQtdC90LjQtSDQuNGFINC90LAg0LrQsNGA0YLQuNC90LrQtV1cbkIgLS0-IHzRgdC_0LjRgdC-0Log0YHQuNC80LLQvtC70L7QsiArINC60YDQsNGB0LjQstCw0Y8g0LrQsNGA0YLQuNC90LrQsHxDW9Ce0L_RgNC10LQuINCy0YvRgdC-0YLRgyDQvdC-0YIg0Lgg0LfQvdCw0LrQvtCyLCDQt9C90LDRjyDQutC-0L7RgNC00LjQvdCw0YLRiyDQuNGFINGG0LXQvdGC0YDQvtCyINC4INC90L7RgtC90L7Qs9C-INGB0YLQsNC90LBdXG5DIC0tPiB80LfQvdCw0LXQvCwg0LrQsNC60YPRjiDQstGL0YHQvtGC0YMg0L3Rg9C20L3QviDRgdGL0LPRgNCw0YLRjHwgRFvQntC_0YDQtdC0LiDQtNC70LjRgtC10LvRjNC90L7RgdGC0Ywg0L3QvtGC0Ysg0YEg0L_QvtC80L7RidGM0Y4g0L3QtdC50YDQvtC90L3QvtC5INGB0LXRgtC4XVxuRCAtLT4gfNC30L3QsNC10LwsINC60LDQutC40LUg0LTQu9C40YLQtdC70YzQvdC-0YHRgtC4INC90YPQttC90L4g0YHRi9Cz0YDQsNGC0Yx8IEVb0J_RgNC10L7QsdGA0LDQt9GD0LXQvCDQsiAqLm1pZCDQv9C-0LvRg9GH0LXQvdC90YvQuSDRgdC_0LjRgdC-0Log0YHQuNC80LLQvtC70L7QsiDQt9C90LDQutC4ICsg0L3QvtGC0YsgKyDQv9Cw0YPQt9GLXSIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)

## 6. Отчет по работе нейросети
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
## 6. links (demo, examples, building, testing)
## 7. TODO
- Обработка диезов, бемолей и бекаров не только при ключе;
- Распознавание нот в басовом ключе;
- Обработка аккордов.

## Выполнили
Бояркина Елизавета, студент группы ИУ8-31 @freesummerwind 

Кидинова Дарья, студент группы ИУ8-31 @ezuryy
