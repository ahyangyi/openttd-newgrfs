# Source
# https://github.com/OpenTTD/OpenTTD/blob/master/src/table/roadveh_movement.h

straight = [0] * 16
right = [0] * 2 + [1] * 4 + [2] * 2
left = [0] * 5 + [-1] * 5 + [-2] * 5
u_turn = [-1, -2, -2, -3]
up = [(i + 1) // 2 for i in range(0, 16)]


def search(n):
    paths = []

    def dfs(cur, heights, history, cutoff, degree, z):
        if n >= 4 and "UU" in history:
            return
        if len(history) == 1 and cutoff == -1:
            for i in range(len(cur)):
                dfs(cur[i:], heights[i:], history, i, degree - cur[i], z)
            return
        if len(cur) >= n:
            paths.append((cur[:n], history, cutoff))
            return
        dfs(cur + [a + degree for a in straight], heights + [z] * 16, history + "S", cutoff, degree, z)
        dfs(cur + [a + degree for a in straight], heights + [z + d for d in up], history + "U", cutoff, degree, z + 8)
        dfs(cur + [a + degree for a in straight], heights + [z - d for d in up], history + "D", cutoff, degree, z - 8)
        dfs(cur + [a + degree for a in right], heights + [z] * 8, history + "R", cutoff, degree + 2, z)
        dfs(cur + [a + degree for a in left], heights + [z] * 15, history + "L", cutoff, degree - 2, z)
        dfs(cur + [a + degree for a in u_turn], heights + [z] * 4, history + "T", cutoff, degree - 4, z)

    dfs([], [], "", -1, 0, 0)
    return paths


def visualize():
    from PIL import Image, ImageDraw

    im = Image.new("RGBA", (400, 400), (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    def coords(x, y, z):
        return 200 + x * 32 - y * 32, 200 + x * 16 + y * 16 - z * 8

    def draw_grid(f, t):
        fx, fy = coords(*f)
        tx, ty = coords(*t)
        draw.line((fx, fy, tx, ty), fill=(0, 0, 0))

    for x in range(-2, 2):
        for y in range(-2, 2):
            draw_grid((x, y, 0), (x, y + 1, 0))
            draw_grid((x, y, 0), (x + 1, y, 0))
            draw_grid((x, y + 1, 0), (x + 1, y + 1, 0))
            draw_grid((x + 1, y, 0), (x + 1, y + 1, 0))

    return im


if __name__ == "__main__":
    for i in search(13):
        print(i)
    visualize().save("x.png")
