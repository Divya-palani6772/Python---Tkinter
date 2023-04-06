import math


class BubbleCursor:
    def __init__(self, canvas, objects, x=0, y=0):
        self.x = x
        self.y = y
        self.radius = 40
        self.canvas = canvas
        self.objects = objects
        self.cursor_size = 7

        # create a bubble cursor: a horizontal segment, a vertical segment, and a circle
        self.cursor_tag_circle = self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius,
                                                         y + self.radius, fill="gray", outline="gray", width=0)
        self.canvas.tag_lower(self.cursor_tag_circle)  # move the cursor's circle to bottom level

        self.cursor_tag_horizontal = self.canvas.create_line(x - self.cursor_size, y, x + self.cursor_size, y,
                                                             fill='black', width=2)
        self.cursor_tag_vertical = self.canvas.create_line(x, y - self.cursor_size, x, y + self.cursor_size,
                                                           fill='black', width=2)

        self.selected_object = -1  # no object has been selected

    def update_cursor(self, x, y):
        # according to the (x, y), update the bubble cursor
        self._determine_selected_object(x, y)
        self.canvas.coords(self.cursor_tag_circle, x - self.radius, y - self.radius, x + self.radius, y + self.radius)
        self.canvas.coords(self.cursor_tag_horizontal, x - self.cursor_size, y, x + self.cursor_size, y)
        self.canvas.itemconfig(self.cursor_tag_horizontal, fill="black", width=2)
        self.canvas.coords(self.cursor_tag_vertical, x, y - self.cursor_size, x, y + self.cursor_size)
        self.canvas.itemconfig(self.cursor_tag_vertical, fill="black", width=2)

    def get_selected_object(self):  # return the index of the selected object in the object list
        return self.selected_object

    def _determine_selected_object(self, x, y):
        intersecting_distance = 0
        containment_distance = 0
        closest_object = -1  # no object has been selected

        # find the closest target overlapping the bubble cursor
        for i in range(len(self.objects)):

            # calculation for intersecting distance
            distance = math.hypot(self.objects[i].x - x, self.objects[i].y - y)
            if i == 0:
                intersecting_distance = distance
                if distance <= (self.radius + self.objects[i].radius):
                    closest_object = i
            else:
                if distance <= (self.radius + self.objects[i].radius) and distance <= intersecting_distance:
                    intersecting_distance = distance
                    closest_object = i

        for j in range(len(self.objects)):

            # calculation for containment distance
            self.radius = 2 * self.radius
            distance = math.hypot(self.objects[j].x - x, self.objects[j].y - y)
            if j == 0:
                containment_distance = distance
                if distance <= (self.radius + self.objects[j].radius):
                    closest_object = j
            else:
                if distance <= (self.radius + self.objects[j].radius) and distance <= containment_distance:
                    containment_distance = distance
                    closest_object = j

        # finding minimum distance
        self.radius = min(intersecting_distance, containment_distance)

        # find the selected object
        self.selected_object = closest_object