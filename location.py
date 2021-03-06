import cv2
import numpy as np
import pandas as pd


def find_scale(image, count_of_iterations, offset, symbol_type, x_coordinate, y_coordinate, widths, heights,
               symbol_types, start_percent, stop_percent, threshold, sub_path):
    """ This function searches template images in input image and returns best scale """

    image_width, image_height = image.shape[::-1]
    best_location_count = -1
    best_locations = []
    best_scale = 1
    best_height = 0
    best_width = 0
    for scale in [j / 100.0 for j in range(start_percent, stop_percent + 1, 5)]:
        locations = []
        location_count = 0
        sum_of_pixels = 0
        average_height = 0
        average_width = 0
        counter = 0
        for i in range(count_of_iterations):
            template = cv2.imread(sub_path + 'templates/' + str(i + offset) + '.png', 0)
            w, h = template.shape[::-1]
            if scale * h > image_height:
                break
            template = cv2.resize(template, None,
                                  fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            min_result, max_result, _, _ = cv2.minMaxLoc(result)
            result = np.where(result > threshold)
            if len(result[0]) != 0:
                sum_of_pixels += result[0].sum()
                location_count = max_result
                locations = result
                average_height += h
                average_width += w
                counter += 1

        if location_count >= best_location_count and counter != 0:
            average_height /= counter
            average_width /= counter
            sum_of_pixels /= location_count
            best_location_count = location_count
            best_locations = locations
            best_scale = scale
            best_height = average_height
            best_width = average_width

    for pt in zip(*best_locations[::-1]):
        x_coordinate.append(pt[0])
        y_coordinate.append(pt[1])
        widths.append(round(best_scale * best_width))
        heights.append(round(best_scale * best_height))
        symbol_types.append(symbol_type)

    return best_scale


def create_table(gray_img, color_img, sub_path=''):
    """ This function searches symbols, creates image with symbols and returns list of found symbols """

    x_coordinate = []
    y_coordinate = []
    widths = []
    heights = []
    type_of_symbol = []

    scale = find_scale(gray_img, 8, 80, 'staff', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 40, 150,
                       0.82, sub_path)
    low_scale = round(100 * scale - 5)
    high_scale = round(100 * scale + 5)

    # NOTE 4 OR NOTE 8
    find_scale(gray_img, 1, 11, 'note8/note4', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.7, sub_path)
    find_scale(gray_img, 1, 14, 'note8/note4', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.7, sub_path)
    find_scale(gray_img, 1, 15, 'note8/note4', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.68, sub_path)
    find_scale(gray_img, 1, 16, 'note8/note4', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.8, sub_path)
    find_scale(gray_img, 1, 18, 'note8/note4', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.85, sub_path)

    # NOTE 2
    find_scale(gray_img, 1, 20, 'note2', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.65, sub_path)
    find_scale(gray_img, 2, 21, 'note2', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.77, sub_path)
    find_scale(gray_img, 1, 23, 'note2', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.7, sub_path)
    find_scale(gray_img, 1, 24, 'note2', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.75, sub_path)
    find_scale(gray_img, 5, 25, 'note2', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.77, sub_path)

    # NOTE 1
    find_scale(gray_img, 1, 30, 'note1', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.78, sub_path)
    find_scale(gray_img, 1, 32, 'note1', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.68, sub_path)
    find_scale(gray_img, 1, 34, 'note1', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.75, sub_path)
    find_scale(gray_img, 1, 36, 'note1', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.75, sub_path)
    find_scale(gray_img, 1, 37, 'note1', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.75, sub_path)

    # FLAT
    find_scale(gray_img, 2, 40, 'flat', x_coordinate, y_coordinate, widths, heights, type_of_symbol,
               low_scale, high_scale, 0.75, sub_path)
    find_scale(gray_img, 1, 42, 'flat', x_coordinate, y_coordinate, widths, heights, type_of_symbol,
               low_scale, high_scale, 0.75, sub_path)
    find_scale(gray_img, 1, 43, 'flat', x_coordinate, y_coordinate, widths, heights, type_of_symbol,
               low_scale, high_scale, 0.75, sub_path)

    # SHARP
    find_scale(gray_img, 1, 50, 'sharp', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.75, sub_path)
    find_scale(gray_img, 1, 51, 'sharp', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.76, sub_path)
    find_scale(gray_img, 1, 53, 'sharp', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.9, sub_path)
    find_scale(gray_img, 2, 54, 'sharp', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.77, sub_path)
    find_scale(gray_img, 2, 56, 'sharp', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.765, sub_path)

    # PAUSE 1
    find_scale(gray_img, 1, 100, 'pause1', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.9, sub_path)

    # PAUSE 2
    find_scale(gray_img, 1, 111, 'pause2', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.8, sub_path)
    find_scale(gray_img, 1, 112, 'pause2', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.8, sub_path)

    # PAUSE 4
    find_scale(gray_img, 1, 120, 'pause4', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.6, sub_path)
    find_scale(gray_img, 1, 121, 'pause4', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.7, sub_path)

    # PAUSE 8
    find_scale(gray_img, 2, 130, 'pause8', x_coordinate, y_coordinate, widths, heights, type_of_symbol, low_scale,
               high_scale, 0.8, sub_path)

    d = {'x': x_coordinate, 'y': y_coordinate, 'width': widths, 'height': heights, 'symbol': type_of_symbol}
    df = pd.DataFrame(data=d)
    df = df.drop_duplicates(subset=['x'])
    df = df.sort_values(by='x')
    df = df.reset_index(drop=True)

    indexes_for_drop = []
    for i in range(df['x'].size - 1):
        if df.loc[i + 1, 'symbol'] != 'staff' and df.loc[i, 'symbol'] != 'staff' \
                and df.loc[i + 1, 'symbol'] == df.loc[i, 'symbol'] \
                and df.loc[i + 1, 'x'] - df.loc[i, 'x'] <= (df.loc[i, 'width'] + 1) / 2:
            df.loc[i + 1, 'x'] = df.loc[i, 'x']
            df.loc[i + 1, 'width'] = df.loc[i + 1, 'x'] - df.loc[i, 'x'] + df.loc[i + 1, 'width']
            indexes_for_drop.append(i)
    df.drop(indexes_for_drop, inplace=True)
    df = df.reset_index(drop=True)

    rectangles_of_staff = []
    for i in range(df['x'].size - 1):
        if df.loc[i, 'symbol'] == 'staff':
            if i == 0:
                rectangles_of_staff.append('start')
            elif df.loc[i - 1, 'symbol'] != 'staff' and df.loc[i + 1, 'symbol'] != 'staff':
                rectangles_of_staff.append('-')
            elif df.loc[i - 1, 'symbol'] != 'staff' and df.loc[i + 1, 'symbol'] == 'staff':
                rectangles_of_staff.append('start')
            elif df.loc[i - 1, 'symbol'] == 'staff' and df.loc[i + 1, 'symbol'] != 'staff':
                rectangles_of_staff.append('end')
            elif df.loc[i - 1, 'symbol'] == 'staff' and df.loc[i + 1, 'symbol'] == 'staff':
                rectangles_of_staff.append('drop')
        else:
            rectangles_of_staff.append('-')

    rectangles_of_staff.append('-')
    df['status'] = rectangles_of_staff

    indexes_for_drop = df[df['status'] == 'drop'].index
    df.drop(indexes_for_drop, inplace=True)
    df = df.reset_index(drop=True)

    for i in range(df['x'].size - 1):
        if df.loc[i, 'status'] == 'start':
            df.loc[i, 'width'] = df.loc[i + 1, 'x'] - df.loc[i, 'x'] + df.loc[i + 1, 'width']
            df.loc[i, 'x'] = df.loc[i, 'x']

    indexes_for_drop = df[df['status'] == 'end'].index
    df.drop(indexes_for_drop, inplace=True)
    df = df.reset_index(drop=True)

    for ind in range(df['x'].size):
        x = df.loc[ind, 'x']
        y = df.loc[ind, 'y']
        width = df.loc[ind, 'width']
        height = df.loc[ind, 'height']
        if df.loc[ind, 'symbol'] == 'sharp' or df.loc[ind, 'symbol'] == 'flat':
            cv2.rectangle(color_img, (x, y), (x + width, y + height), (0, 100, 0), 2)
        elif df.loc[ind, 'symbol'] == 'staff':
            cv2.rectangle(color_img, (x, y), (x + width, y + height), (0, 0, 255), 2)
        elif df.loc[ind, 'symbol'] == 'note8/note4':
            if ind == 0 and df.loc[ind + 1, 'symbol'] == 'staff':
                cv2.rectangle(color_img, (x, y), (x + width, y + height), (255, 0, 255), 2)
                df.loc[ind, 'symbol'] = 'note4'
            elif ind == 0:
                cv2.rectangle(color_img, (x, y), (x + width, y + height), (220, 0, 100), 2)  # note8
                df.loc[ind, 'symbol'] = 'note8'
            elif ind == df['x'].size and df.loc[ind - 1, 'symbol'] == 'staff':
                cv2.rectangle(color_img, (x, y), (x + width, y + height), (255, 0, 255), 2)
                df.loc[ind, 'symbol'] = 'note4'
            elif ind == df['x'].size:
                cv2.rectangle(color_img, (x, y), (x + width, y + height), (255, 0, 255), 2)
                df.loc[ind, 'symbol'] = 'note8'
            elif df.loc[ind - 1, 'symbol'] == 'staff' and df.loc[ind + 1, 'symbol'] == 'staff':  # note4
                cv2.rectangle(color_img, (x, y), (x + width, y + height), (255, 0, 255), 2)
                df.loc[ind, 'symbol'] = 'note4'
            else:
                cv2.rectangle(color_img, (x, y), (x + width, y + height), (220, 0, 100), 2)  # note8
                df.loc[ind, 'symbol'] = 'note8'
        elif df.loc[ind, 'symbol'] == 'note2':
            cv2.rectangle(color_img, (x, y), (x + width, y + height), (0, 255, 255), 2)
        elif df.loc[ind, 'symbol'] == 'note1':
            cv2.rectangle(color_img, (x, y), (x + width, y + height), (0, 130, 255), 2)
        else:
            cv2.rectangle(color_img, (x, y), (x + width, y + height), (255, 130, 0), 2)

    cv2.imwrite('result.png', color_img)
    return df
