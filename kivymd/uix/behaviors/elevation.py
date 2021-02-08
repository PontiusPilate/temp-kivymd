"""
Behaviors/Elevation
===================

.. rubric:: Classes implements a circular and rectangular elevation effects.

To create a widget with rectangular or circular elevation effect,
you must create a new class that inherits from the
:class:`~RectangularElevationBehavior` or :class:`~CircularElevationBehavior`
class.

For example, let's create an button with a rectangular elevation effect:

.. code-block:: python

    from kivy.lang import Builder
    from kivy.uix.behaviors import ButtonBehavior

    from kivymd.app import MDApp
    from kivymd.uix.behaviors import (
        RectangularRippleBehavior,
        BackgroundColorBehavior,
        RectangularElevationBehavior,
    )

    KV = '''
    <RectangularElevationButton>:
        size_hint: None, None
        size: "250dp", "50dp"


    Screen:

        # With elevation effect
        RectangularElevationButton:
            pos_hint: {"center_x": .5, "center_y": .6}
            elevation: 11

        # Without elevation effect
        RectangularElevationButton:
            pos_hint: {"center_x": .5, "center_y": .4}
    '''


    class RectangularElevationButton(
        RectangularRippleBehavior,
        RectangularElevationBehavior,
        ButtonBehavior,
        BackgroundColorBehavior,
    ):
        md_bg_color = [0, 0, 1, 1]


    class Example(MDApp):
        def build(self):
            return Builder.load_string(KV)


    Example().run()

.. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/rectangular-elevation-effect.gif
    :align: center

Similarly, create a button with a circular elevation effect:

.. code-block:: python

    from kivy.lang import Builder
    from kivy.animation import Animation
    from kivy.uix.image import Image
    from kivy.uix.behaviors import ButtonBehavior
    from kivymd.uix.label import  MDIcon
    from kivymd.app import MDApp
    from kivymd.uix.behaviors import (
        CircularRippleBehavior,
        CircularElevationBehavior,
        SpecificBackgroundColorBehavior
    )
    from kivy.uix.boxlayout import BoxLayout
    from kivy.properties import ObjectProperty

    KV = '''
    #:import images_path kivymd.images_path
    #:import Animation kivy.animation.Animation

    <CircularElevationButton>:
        size_hint: None, None
        size: "100dp", "100dp"
        source: f"{images_path}/kivymd.png"
        anima:Animation
        radius: self.size[0]/2
        elevation:10
        MDIcon:
            icon:"hand-heart"
            halign:"center"
            valign:"center"
            size:root.size
            pos:root.pos
            font_size:root.size[0]*0.6
            theme_text_color:"Custom"
            text_color:[1]*4


    Screen:

        # With elevation effect
        CircularElevationButton:
            pos_hint: {"center_x": .5, "center_y": .6}
            elevation: 5

        # Without elevation effect
        CircularElevationButton:
            pos_hint: {"center_x": .5, "center_y": .4}
            elevation: 0
    '''


    class CircularElevationButton(
        CircularElevationBehavior,
        CircularRippleBehavior,
        SpecificBackgroundColorBehavior,
        ButtonBehavior,
        BoxLayout,
    ):
        md_bg_color = [0, 0, 1, 1]
        shadow_animation=ObjectProperty()

        def on_press(self,*dt):
            if self.shadow_animation:
                Animation.cancel(self.shadow_animation)
            Animation(_elevation=30, d=0.2).start(self)

        def on_release(self,*dt):
            if self.shadow_animation:
                Animation.cancel(self.shadow_animation)
            Animation(_elevation=self.elevation, d=0.2).start(self)


    class Example(MDApp):
        def build(self):
            return Builder.load_string(KV)


    Example().run()


.. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/circular-elevation-effect.gif
    :align: center
"""

__all__ = (
    "CommonElevationBehavior",
    "RectangularElevationBehavior",
    "CircularElevationBehavior",
    "RoundedRectangularElevationBehavior",
)

from io import BytesIO
from weakref import WeakMethod, ref

from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    AliasProperty,
    BoundedNumericProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    ReferenceListProperty,
    StringProperty,
    VariableListProperty,
)
from kivy.uix.widget import Widget
from PIL import Image, ImageDraw, ImageFilter

Builder.load_string(
    """
#:import InstructionGroup kivy.graphics.instructions.InstructionGroup
<CommonElevationBehavior>
    canvas.before:
        # SOFT SHADOW
        PushMatrix:
        Rotate:
            angle:self.angle
            origin: self._shadow_origin
        Color:
            group:"soft_shadow"
            rgba:root.soft_shadow_cl
        Rectangle:
            group:"soft_shadow"
            texture: self._soft_shadow_texture
            size: self.soft_shadow_size
            pos: self.soft_shadow_pos
        PopMatrix:
        # HARD SHADOW
        PushMatrix:
        Rotate:
            angle:self.angle
            origin: self.center
        Color:
            group:"hard_shadow"
            rgba:root.hard_shadow_cl
        Rectangle:
            group:"hard_shadow"
            texture: self.hard_shadow_texture
            size: self.hard_shadow_size
            pos: self.hard_shadow_pos
        PopMatrix:
        Color:
            group:"shadow"
            a: 1
""",
    filename="CommonElevationBehavior.kv",
)


class CommonElevationBehavior(Widget):
    """Common base class for rectangular and circular elevation behavior."""

    elevation = BoundedNumericProperty(0, min=0)
    """
    Elevation of the widget

    .. note::

        Altho this value does not represent the current elevation of the widget.
        _elevation can be used to animate the current elevation and come back
        using the `elevation` property directly.

        For example:

        .. code-block:: kv

            <Widget_with_shadow>:
                on_press:
                    Animation.cancel_all(self)
                    Animation(_elevation = 10, d=1).start(widget)
                on_release:
                    Animation.cancel_all(self)
                    Animation(_elevation = self.elevation).start(self)


    """

    # Shadow rendering porpoerties
    # Shadow rotation meomry - SHARED ACROSS OTHER CLASSES
    angle = NumericProperty(0)
    """
    Angle of rotation in degrees of the current shadow.
    This value is shared across different widgets.

    .. note::

        This value will affect both, hard and soft shadows.
        Each shadow has his own origin point that's computed every time the
        elevation changes.

    :attr:`angle` is an :class:`~kivy.properties.NumericProperty`
    and defaults to 0.
    """
    radius = VariableListProperty([0])
    """
    Radious of the Corners of the shadow.
    this values represents each corner of the shadow, starting from top-left
    corner and going clockwise.

    .. code-block:: python

        radius = [
            "top-left",
            "top-right",
            "bottom-right",
            "bottom-left",
        ]

    This value can be expanded thus allowing this settings to be valid:

    .. code-block:: python

        widget.radius=[0] # Translates to [0,0,0,0]
        widget.radius=[10,3] # Translates to [10,3,10,3]
        widget.radius=[7.0,8.7,1.5,3.0] # Translates to [7,8,1,3]


    .. note::

        This value will affect both, hard and soft shadows.
        this value only affects RoundedRectangularElevationBehavior for now,
        but can be stored and used by custom shadow Draw functions.

    :attr:`radius` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to [0, 0, 0, 0].
    """

    # Position of the shadow
    _shadow_origin_x = NumericProperty(0)
    """
    Shadow origin x position for the rotation origin.
    managed by _shadow_origin.

    :attr:`_shadow_origin_x` is an :class:`~kivy.properties.NumericProperty`
    and defaults to 0.

    .. note::
        This property is automatically procesed. by _shadow_origin
    """

    _shadow_origin_y = NumericProperty(0)
    """
    Shadow origin y position for the rotation origin.
    managed by _shadow_origin.

    :attr:`_shadow_origin_y` is an :class:`~kivy.properties.NumericProperty`
    and defaults to 0.

    .. note::
        This property is automatically procesed.
    """

    _shadow_origin = ReferenceListProperty(_shadow_origin_x, _shadow_origin_y)
    """
    Soft Shadow Rotation origin point.

    :attr:`shadow_y` is an :class:`~kivy.properties.ReferenceListProperty`
    and defaults to `[0,0]`.

    .. note::

        This property is automatically procesed and relative to the canvas center.
    """

    _shadow_pos = ListProperty([0, 0])  # custom offset
    """
    Soft Shadow origin point.

    :attr:`shadow_y` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[0, 0]`.

    .. note::
        This property is automatically procesed and relative to the Widget's
        canvas center.
    """

    shadow_pos = ListProperty([0, 0])  # bottom left corner
    """
    Custom shadow Origin point. if this property is set, _shadow_pos will be
    ommited.

    This property allows userts to fake light source.

    :attr:`soft_shadow_size` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[0, 0]`.

    .. note::
        this value overwrite the _shadow_pos processing
    """

    # Shadow Group shared memory
    __shadow_groups = {"global": []}
    shadow_group = StringProperty("global")
    """
    Widget's shadow Group.
    by deffault every widget with a shadow is saved inside the memory
    __shadow_groups. as a weakref. this means that you can have multiple
    light sources, one for every shadow group.

    To fake a light source use force_shadow_pos.

    :attr:`elevation` is an :class:`~kivy.properties.StringProperty`
    and defaults to `"global"`.
    """

    _elevation = NumericProperty(0)
    """
    inner memory for the elevation.

    .. warning::
    This property is the current elevation of the widget, do not use this
    property directly, instead, use CommonElevationBehavior.elevation.

    :attr:`elevation` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    """
    # soft shadow
    _soft_shadow_texture = ObjectProperty()
    """
    Texture of the Soft Shadow texture for the canvas.

    :attr:`soft_shadow_texture` is an :class:`~kivy.core.image.Image`
    and defaults to `None`.

    .. note::
        This property is automatically procesed.
    """
    soft_shadow_size = ListProperty((0, 0))
    """
    Size of the soft Shadow texture over the canvas.

    :attr:`soft_shadow_size` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[0, 0]`.

    .. note::
        This property is automatically procesed.
    """
    soft_shadow_pos = ListProperty((0, 0))
    """
    Position of the Hard Shadow texture over the canvas.

    :attr:`soft_shadow_pos` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[0, 0]`.

    .. note::
        This property is automatically procesed.
    """
    soft_shadow_cl = ListProperty([0, 0, 0, 0.50])
    """
    Color of the soft Shadow

    :attr:`soft_shadow_cl` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[0, 0, 0, 0.15]`.
    """

    # hard shadow
    hard_shadow_texture = ObjectProperty()
    """
    Texture of the Hard Shadow texture for the canvas.

    :attr:`hard_shadow_texture` is an :class:`~kivy.core.image.Image`
    and defaults to `None`.

    .. note::
        This property is automatically procesed when elevation is changed.
    """

    hard_shadow_size = ListProperty((0, 0))
    """
    Size of the Hard Shadow texture over the canvas.

    :attr:`hard_shadow_size` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[0, 0]`.

    .. note::
        This property is automatically procesed when elevation is changed.
    """

    hard_shadow_pos = ListProperty((0, 0))
    """
    Position of the Hard Shadow texture over the canvas.

    :attr:`hard_shadow_pos` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[0, 0]`.

    .. note::
        This property is automatically procesed when elevation is changed.
    """

    hard_shadow_cl = ListProperty([0, 0, 0, 0.15])
    """
    Color of the Hard Shadow.

    .. note::
        :attr:`hard_shadow_cl` is an :class:`~kivy.properties.ListProperty`
        and defaults to `[0, 0, 0, 0.15]`.
    """
    # shared property for some calculations.
    hard_shadow_offset = BoundedNumericProperty(
        2, min=0, errorhandler=lambda x: 0 if x < 0 else x
    )
    """
    This value sets a special offset to the shadow canvas, this offset allows a
    correct draw of the canvas size. allowing the effect to correctly blur the
    image in the given space.

    :attr:`hard_shadow_offset` is an :class:`~kivy.properties.BoundedNumericProperty`
    and defaults to `2`.
    """

    soft_shadow_offset = BoundedNumericProperty(
        4, min=0, errorhandler=lambda x: 0 if x < 0 else x
    )
    """
    This value sets a special offset to the shadow canvas, this offset allows a
    correct draw of the canvas size. allowing the effect to correctly blur the
    image in the given space.

    :attr:`soft_shadow_offset` is an :class:`~kivy.properties.BoundedNumericProperty`
    and defaults to `4`.
    """

    draw_shadow = ObjectProperty(None)
    """
    This property controls the draw call of the context.

    This property is automatically set to `__draw_shadow__` inside the
    `super().__init__ call.` unless the property is different of None.

    To set a different drawing instruction function, set this property before the
    `super(),__init__` call inside the `__init__` definition of the new class.

    You can use the source for this clases as example of how to draw over
    with the context:

    #. "RectangularElevationBehavior"
    #. "CircularElevationBehavior"
    #. "RoundedRectangularElevationBehavior"

    :attr:`draw_shadow` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to None.

    .. note::
        if this property is left to None the CommonElevationBehavior will set
        to a function that will raise a `NotImplementedError` inside
        `super().__init__`.

    Follow the next example to set a new draw instruction for the class
    inside `__init__`:

    .. code-block:: python

        class RoundedRectangularElevationBehavior(CommonElevationBehavior):
            "Shadow Class for the RoundedRectangule shadow behavior.
            Controls the size and position of the shadow."

            def __init__(self, **kwargs):
                self._draw_shadow = WeakMethod(self.__draw_shadow__)
                super().__init__(**kwargs)

            def __draw_shadow__(self, origin, end, context=None):
                context.draw(...)

    Context is a Pillow `ImageDraw` class.
    for more information check the Pillow official documentation.
    """

    def __init__(self, **kwargs):
        if self.draw_shadow is None:
            self.draw_shadow = WeakMethod(self.__draw_shadow__)
        self.prev_shadow_group = None
        im = BytesIO()
        Image.new("RGBA", (4, 4), color=(0, 0, 0, 0)).save(im, format="png")
        im.seek(0)
        #
        self._soft_shadow_texture = self.hard_shadow_texture = CoreImage(
            im, ext="png"
        ).texture
        Clock.schedule_once(self.shadow_preset, -1)
        self.on_shadow_group(self, self.shadow_group)

        self.bind(
            pos=self._update_shadow,
            size=self._update_shadow,
            radius=self._update_shadow,
        )
        super().__init__(**kwargs)

    #

    def on_shadow_group(self, instance, value):
        """
        This function controls the shadow group of the widget.
        Do not use Directly to change the group. instead, use the shadow_group
        :attr:`property`.
        """
        groups = CommonElevationBehavior.__shadow_groups
        if self.prev_shadow_group:
            group = groups[self.prev_shadow_group]
            for widget in group[:]:
                if widget() is self:
                    group.remove(widget)
        group = self.prev_shadow_group = self.shadow_group
        if group not in groups:
            groups[group] = []
        r = ref(self, CommonElevationBehavior._clear_shadow_groups)
        groups[group].append(r)

    #
    @staticmethod
    def _clear_shadow_groups(wk):
        # auto flush the element when the weak reference have been deleted
        groups = CommonElevationBehavior.__shadow_groups
        for group in list(groups.values()):
            if not group:
                break
            if wk in group:
                group.remove(wk)
                break

    def force_shadow_pos(self, shadow_pos):
        """
        This property forces the shadow position in every widget inside the
        widget.
        the argument :attr:`shadow_pos` is expected as a List or Tuple.
        """
        if self.shadow_group is None:
            return
        group = CommonElevationBehavior.__shadow_groups[self.shadow_group]
        for wk in group[:]:
            widget = wk()
            if widget is None:
                group.remove(wk)
            widget.shadow_pos = shadow_pos
        del group

    #
    def update_group_property(self, property_name, value):
        """
        This functions allows to change properties of every widget inside the
        shadow group.
        """
        if self.shadow_group is None:
            return
        group = CommonElevationBehavior.__shadow_groups[self.shadow_group]
        for wk in group[:]:
            widget = wk()
            if widget is None:
                group.remove(wk)
            setattr(widget, property_name, value)
        del group

    def shadow_preset(self, *dt):
        """
        This function is meant to set the deffault configuration of the
        elevation.

        After a new instance is created, the elevation property will be launched
        and thus this function will update the elevation if the KV lang have not
        done it already.

        Works similar to an `__after_init__` call inside a widget.
        """
        if self.elevation is None:
            self.elevation = 10
        self._update_shadow(self, self.elevation)
        self.bind(
            pos=self._update_shadow,
            size=self._update_shadow,
            _elevation=self._update_shadow,
        )

    #
    def on_elevation(self, instance, value):
        """
        Elevation event that sets the current elevation value to _elevation
        """
        if value is not None:
            self._elevation = value

    def _set_soft_shadow_a(self, value):
        value = 0 if value < 0 else (1 if value > 1 else value)
        self.soft_shadow_cl[-1] = value
        return True

    def _set_hard_shadow_a(self, value):
        value = 0 if value < 0 else (1 if value > 1 else value)
        self.hard_shadow_cl[-1] = value
        return True

    def _get_soft_shadow_a(self):
        return self.soft_shadow_cl[-1]

    def _get_hard_shadow_a(self):
        return self.hard_shadow_cl[-1]

    _soft_shadow_a = AliasProperty(
        _get_soft_shadow_a, _set_soft_shadow_a, bind=["soft_shadow_cl"]
    )
    _hard_shadow_a = AliasProperty(
        _get_hard_shadow_a, _set_hard_shadow_a, bind=["hard_shadow_cl"]
    )

    def on_disabled(self, instance, value):
        """
        This function hides the shadow when the widget is disabled.
        it sets the shadow to 0.
        """
        if self.disabled is True:
            self._elevation = 0
        else:
            self._elevation = 0 if self.elevation is None else self.elevation
        self._update_shadow(self, self._elevation)
        try:
            super().on_disabled(instance, value)
        except Exception:
            pass

    #
    def _update_elevation(self, instance, value):
        self._elevation = value
        self._update_shadow(instance, value)

    def _update_shadow_pos(self, instance, value):
        self.hard_shadow_pos = [
            self.x - dp(self.hard_shadow_offset),  # + self.shadow_pos[0],
            self.y - dp(self.hard_shadow_offset),  # + self.shadow_pos[1],
        ]
        if self.shadow_pos == [0, 0]:
            self.soft_shadow_pos = [
                self.x
                + self._shadow_pos[0]
                - self._elevation
                - dp(self.soft_shadow_offset),
                self.y
                + self._shadow_pos[1]
                - self._elevation
                - dp(self.soft_shadow_offset),
            ]
        else:
            self.soft_shadow_pos = [
                self.x
                + self.shadow_pos[0]
                - self._elevation
                - dp(self.soft_shadow_offset),
                self.y
                + self.shadow_pos[1]
                - self._elevation
                - dp(self.soft_shadow_offset),
            ]
        self._shadow_origin = [
            self.soft_shadow_pos[0] + self.soft_shadow_size[0] / 2,
            self.soft_shadow_pos[1] + self.soft_shadow_size[1] / 2,
        ]

    def on__shadow_pos(self, ins, val):
        """
        Updates the shadow with the computed value.

        Call this function every time you need to force a shadow update.
        """
        self._update_shadow_pos(ins, val)

    def on_shadow_pos(self, ins, val):
        """
        Updates the shadow with the fixed value.

        Call this function every time you need to force a shadow update.
        """
        self._update_shadow_pos(ins, val)

    def _update_shadow(self, instance, value):
        self._update_shadow_pos(instance, value)
        if self._elevation > 0:
            # dynamic elecation position for the shadow
            if self.shadow_pos == [0, 0]:
                self._shadow_pos = [0, -self._elevation * 0.4]
            # HARD Shadow
            offset = int(dp(self.hard_shadow_offset))
            size = [
                int(self.size[0] + (offset * 2)),
                int(self.size[1] + (offset * 2)),
            ]
            im = BytesIO()
            # Context
            img = Image.new("RGBA", tuple(size), color=(0, 0, 0, 0))
            # Draw context
            shadow = ImageDraw.Draw(img)
            self.draw_shadow()(
                [offset, offset],
                [
                    int(size[0] - 1 - offset),
                    int(size[1] - 1 - offset),
                ],
                context=shadow
                # context=ref(shadow)
            )
            img = img.filter(
                ImageFilter.GaussianBlur(
                    radius=int(dp(1 + self.hard_shadow_offset / 3))
                )
            )
            img.save(im, format="png")
            im.seek(0)
            self.hard_shadow_size = size
            self.hard_shadow_texture = CoreImage(im, ext="png").texture

            # soft shadow
            offset = dp(self.soft_shadow_offset)
            size = [
                int(self.size[0] + dp(self._elevation * 2) + (offset * 2)),
                int(self.size[1] + dp(self._elevation * 2) + (offset * 2)),
                # ((self._elevation)*2) + x + (offset*2)) for x in self.size
            ]
            im = BytesIO()
            img = Image.new("RGBA", tuple(size), color=((0,) * 4))
            shadow = ImageDraw.Draw(img)
            _offset = int(dp(self._elevation + offset))
            self.draw_shadow()(
                [
                    _offset,
                    _offset,
                ],
                [int(size[0] - _offset - 1), int(size[1] - _offset - 1)],
                context=shadow
                # context=ref(shadow)
            )
            img = img.filter(
                ImageFilter.GaussianBlur(radius=self._elevation // 2)
            )
            shadow = ImageDraw.Draw(img)
            #
            img.save(im, format="png")
            im.seek(0)
            self.soft_shadow_size = size
            self._soft_shadow_texture = CoreImage(im, ext="png").texture
        else:
            im = BytesIO()
            Image.new("RGBA", (4, 4), color=(0, 0, 0, 0)).save(im, format="png")
            im.seek(0)
            #
            self._soft_shadow_texture = self.hard_shadow_texture = CoreImage(
                im, ext="png"
            ).texture
            return

    def __draw_shadow__(self, origin, end, context=None):
        raise NotImplementedError(
            "KivyMD:\n"
            "If you see this error, this means that either youre using "
            "CommonElevationBehavior directly or your 'shader' dont have a "
            "_draw_shadow instruction, remember to overwrite this function to "
            "draw over the image context. the figure you would like."
        )


class RectangularElevationBehavior(CommonElevationBehavior):
    """
    Base class for a Rectangular elevation behavior.
    """

    def __init__(self, **kwargs):
        self.draw_shadow = WeakMethod(self.__draw_shadow__)
        super().__init__(**kwargs)

    def __draw_shadow__(self, origin, end, context=None):
        context.rectangle(origin + end, fill=tuple([255] * 4))


class CircularElevationBehavior(CommonElevationBehavior):
    """
    Base class for a Circular elevation behavior.
    """

    def __init__(self, **kwargs):
        self.draw_shadow = WeakMethod(self.__draw_shadow__)
        super().__init__(**kwargs)

    def __draw_shadow__(self, origin, end, context=None):
        context.ellipse(origin + end, fill=tuple([255] * 4))


class RoundedRectangularElevationBehavior(CommonElevationBehavior):
    """
    Base class for RoundedRectangule elevation behavior.
    """

    def __init__(self, **kwargs):
        self.draw_shadow = WeakMethod(self.__draw_shadow__)
        super().__init__(**kwargs)

    def __draw_shadow__(self, origin, end, context=None):
        if self.radius == [0, 0, 0, 0]:
            context.rectangle(origin + end, fill=tuple([255] * 4))
        else:
            radius = [x * 2 for x in self.radius]
            context.pieslice(
                [
                    origin[0],
                    origin[1],
                    origin[0] + radius[0],
                    origin[1] + radius[0],
                ],
                180,
                270,
                fill=(255, 255, 255, 255),
            )
            context.pieslice(
                [
                    end[0] - radius[1],
                    origin[1],
                    end[0],
                    origin[1] + radius[1],
                ],
                270,
                360,
                fill=(255, 255, 255, 255),
            )
            context.pieslice(
                [
                    end[0] - radius[2],
                    end[1] - radius[2],
                    end[0],
                    end[1],
                ],
                0,
                90,
                fill=(255, 255, 255, 255),
            )
            context.pieslice(
                [
                    origin[0],
                    end[1] - radius[3],
                    origin[0] + radius[3],
                    end[1],
                ],
                90,
                180,
                fill=(255, 255, 255, 255),
            )
            if all((x == self.radius[0] for x in self.radius)):
                radius = int(self.radius[0])
                context.rectangle(
                    [
                        origin[0] + radius,
                        origin[1],
                        end[0] - radius,
                        end[1],
                    ],
                    fill=(255,) * 4,
                )
                context.rectangle(
                    [
                        origin[0],
                        origin[1] + radius,
                        end[0],
                        end[1] - radius,
                    ],
                    fill=(255,) * 4,
                )
            else:
                radius = [
                    max((self.radius[0], self.radius[1])),
                    max((self.radius[1], self.radius[2])),
                    max((self.radius[2], self.radius[3])),
                    max((self.radius[3], self.radius[0])),
                ]
                context.rectangle(
                    [
                        origin[0] + self.radius[0],
                        origin[1],
                        end[0] - self.radius[1],
                        end[1] - radius[2],
                    ],
                    fill=(255,) * 4,
                )
                context.rectangle(
                    [
                        origin[0] + radius[3],
                        origin[1] + self.radius[1],
                        end[0],
                        end[1] - self.radius[2],
                    ],
                    fill=(255,) * 4,
                )
                context.rectangle(
                    [
                        origin[0] + self.radius[3],
                        origin[1] + radius[0],
                        end[0] - self.radius[2],
                        end[1],
                    ],
                    fill=(255,) * 4,
                )
                context.rectangle(
                    [
                        origin[0],
                        origin[1] + self.radius[0],
                        end[0] - radius[2],
                        end[1] - self.radius[3],
                    ],
                    fill=(255,) * 4,
                )
