import cartesian
import turtle


class DetailedShape:
    def __init__(self, shape, **details):
        self.shape = shape
        self.details = details


class Canvas:
    def __init__(self, engine):
        self.render_engine = engine
        self.render_queue = []
        self.complete_queue = []

    def __len__(self):
        return len(self.render_queue) + len(self.complete_queue)

    def __getitem__(self, index):
        if index >= len(self.render_queue):
            return self.complete_queue[index - len(self.render_queue)]
        else:
            return self.render_queue[index]

    def __setitem__(self, index, value):
        if index >= len(self.render_queue):
            self.complete_queue[index - len(self.render_queue)] = value
        else:
            self.render_queue[index] = value

    def __delitem__(self, index):
        if index >= len(self.render_queue):
            del self.complete_queue[index - len(self.render_queue)]
        else:
            del self.render_queue[index]

    def __contains__(self, shape):
        return shape in self.render_queue or shape in self.complete_queue

    def __iter__(self):
        return self.render_queue + self.complete_queue

    def append(self, shape):
        self.render_queue.append(shape)

    def extend(self, li):
        self.render_queue.extend(li)

    def remove(self, value):
        if value in self.complete_queue:
            self.complete_queue.remove(value)
        else:
            self.render_queue.remove(value)

    def pop(self, index):
        self.__delitem__(self, index)

    def init(self):
        self.render_engine.init()

    def close(self):
        self.render_engine.close()

    def render_one(self):
        self.render_engine.render(self.render_queue[0])
        self.complete_queue.append(self.render_queue.pop(0))

    def render(self):
        for shape in self.render_queue:
            self.render_engine.render(shape)
        self.complete_queue.extend(self.render_queue)
        self.render_queue = []

    def render_all(self):
        self.render_queue.extend(self.complete_queue)
        self.complete_queue = []
        self.render()

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        del self


class RenderEngine:
    def init(self):
        raise NotImplementedError
        return NotImplemented

    def close(self):
        raise NotImplementedError
        return NotImplemented

    def render(self, shape):
        raise NotImplementedError
        return NotImplemented


class BuiltinTurtleRenderer(RenderEngine):
    def __init__(
        self,
        pen=turtle.Turtle(undobuffersize=1, visible=False),
        ray_length=65535,
        default_color=None,
    ):
        self.canvas = turtle.Screen()
        self.pen = pen
        self.ray_length = ray_length
        if default_color is None:
            default_color = pen.pencolor()
        self.default_color = default_color

    def init(self):
        self.canvas.resetscreen()

    def close(self):
        self.canvas.update()
        self.canvas.mainloop()

    def render(self, shape):
        details = {}
        if isinstance(shape, DetailedShape):
            details = shape.details
            shape = shape.shape
        if hasattr(shape, "render"):
            shape.render(self, details)
        elif isinstance(shape, cartesian.Vector):
            size = 4
            color = self.default_color
            if "size" in details:
                size = details["size"]
            if "color" in details:
                color = details["color"]
            self.pen.penup()
            self.pen.setpos(shape.x, shape.y)
            self.pen.pendown()
            self.pen.dot(size, color)
        elif isinstance(shape, cartesian.Line):
            size = 1
            color = self.default_color
            fill = 0
            fill_color = self.default_color
            if "size" in details:
                size = details["size"]
            if "color" in details:
                color = details["color"]
            if "fill" in details:
                fill = details["fill"]
            if "fill_color" in details:
                fill_color = details["fill_color"]
            self.pen.penup()
            self.pen.setpos(shape.begin.x, shape.begin.y)
            self.pen.pendown()
            heading = self.pen.towards(shape.end.position)
            self.pen.setheading(heading)
            if fill == 1:
                self.pen.begin_fill()
            if isinstance(shape, cartesian.Ray):
                self.pen.forward(self.ray_length)
            elif isinstance(shape, cartesian.Curve):
                self.pen.setpos(shape.end.x, shape.end.y)
            else:
                self.pen.forward(self.ray_length)
                # self.pen.penup()
                self.pen.backward(self.ray_length * 2)
                # self.pen.pendown()
                # self.pen.backward(self.ray_length)
            if fill == -1:
                self.pen.fillcolor(fill_color)
                self.pen.end_fill()


ENABLE_DEBUG = True


def pos_debugger(x, y):
    if ENABLE_DEBUG:
        print("x:{x} y:{y}".format(x=int(x), y=int(y)))


turtle.onscreenclick(pos_debugger)
