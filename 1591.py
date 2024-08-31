from typing import List

class Solution:
    def isPrintable(self, grid: List[List[int]]) -> bool:

        # look for top left and bottom right corners of rectangles
        # find outmost top, left, bottom, and right for each number
        def build():
            for i in range(m):
                for j in range(n):
                    num = grid[i][j]

                    if num not in rects:
                        rects[num] = [i, j, i, j]
                    else:
                        top, left, bottom, right = rects[num]

                        if i < top:
                            rects[num][0] = i
                        if j < left:
                            rects[num][1] = j

                        if i > bottom:
                            rects[num][2] = i
                        if j > right:
                            rects[num][3] = j

            # sort by smallest rectangle
            sorted_rects = sorted(
                rects.items(),
                key=lambda r: (
                    (r[1][2] - r[1][0] + 1) * (r[1][3] - r[1][1] + 1)
                )
            )

            rects.clear()
            rects.update(sorted_rects)


        # check if a rectangle is blocked
        def blocked(num):
            if num not in blockers:
                return False

            if blockers[num] in rects:
                return True

            del blockers[num]

            return False

        # for each top left, see if we can reach bottom right
        def check_nums():
            for num in rects.keys():
                if blocked(num):
                    continue

                top, left, bottom, right = rects[num]
                t, l, b, r = top, left, bottom, right

                # see if it's a full rectangle
                is_rectangle = True
                while t != b or l != r:

                    if grid[t][l] != num and grid[t][l] not in used:
                        blockers[num] = grid[t][l]
                        is_rectangle = False
                        break

                    l += 1
                    if l == r + 1 and t < b:
                        t, l = t + 1, left


                # if it's a full rectangle, delete it
                if is_rectangle is True:
                    return True, num

            return False, None


        # TOP LEFT BOTTOM RIGHT

        # find full rectangles and attempt to go backwards
        m = len(grid)
        n = len(grid[0])

        used = set()
        rects = {}  # rects[num] = [top, left, bottom, right]
        blockers = {}  # blockers[num] = num

        build()

        while rects:
            found, num = check_nums()

            if found is False:
                return False

            rects.pop(num)
            used.add(num)

            if not rects:
                return True

        return True


s = Solution()

c1 = [[1,1,1,1],
      [1,2,2,1],
      [1,2,2,1],
      [1,1,1,1]]

c2 = [[1,1,1,1],
      [1,1,3,3],
      [1,1,3,4],
      [5,5,1,4]]

c3 = [[1,2,1],
      [2,1,2],
      [1,2,1]]

print(s.isPrintable(c1))
print(s.isPrintable(c2))
print(s.isPrintable(c3))

