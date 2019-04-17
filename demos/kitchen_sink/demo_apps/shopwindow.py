from kivy.app import App
from kivy.metrics import dp
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation

from kivymd.theming import ThemableBehavior

screen_shop_window = '''
#:import MDCard kivymd.cards.MDCard
#:import MDSeparator kivymd.cards.MDSeparator
#:import MDLabel kivymd.label.MDLabel
#:import MDFlatButton kivymd.button.MDFlatButton
#:import MDRaisedButton kivymd.button.MDRaisedButton
#:import MDFillRoundFlatButton kivymd.button.MDFillRoundFlatButton
#:import MDIconButton kivymd.button.MDIconButton
#:import MDBottomNavigation kivymd.tabs.MDBottomNavigation
#:import MDTextFieldRect kivymd.textfields.MDTextField
#:import images_path kivymd.images_path


<BaseDialog>
    background: '{}/transparent.png'.format(images_path)

    canvas.before:
        Color:
            rgba: root.canvas_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [15,]


<PreviousDialog>
    size_hint: 0, 0

    BoxLayout:
        padding: dp(10)

        Image:
            source: root.icon


<MyRecycleView@RecycleView>
    key_viewclass: 'viewclass'
    key_size: 'height'

    RecycleBoxLayout:
        padding: dp(10)
        spacing: dp(10)
        default_size: None, dp(48)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'


<CardItemForCart@MDCard>
    orientation: 'vertical'
    spacing: dp(20)
    padding: dp(10)
    product_image: ''

    BoxLayout:
        spacing: dp(10)

        Image:
            source: root.product_image
            size_hint: None, None
            size: dp(75), dp(150)

        BoxLayout:
            orientation: 'vertical'

            MDLabel:
                theme_text_color: 'Primary'
                font_style: 'Subtitle1'
                text: '\\n' + 'Casio CVD-12L'
                height: self.texture_size[1]
                size_hint_y: None
                bold: True

            MDLabel:
                theme_text_color: 'Primary'
                text: 'Number: 1234567890'
                height: self.texture_size[1]
                size_hint_y: None

            Widget:

            MDLabel:
                theme_text_color: 'Primary'
                font_style: 'Subtitle1'
                text: 'Price - 850 $'
                height: self.texture_size[1]
                size_hint_y: None
                bold: True

        MDIconButton:
            icon: 'close'
            pos_hint: {'top': 1}


<CardItemForShopWindow@MDCard>
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(5)
    icon: ''
    previous_dialog: None

    AnchorLayout:
        anchor_x: 'right'
        size_hint_y: None
        height: dp(30)

        MDIconButton:
            icon: 'heart-outline'
            theme_text_color: 'Custom'
            text_color: app.theme_cls.primary_color
            on_press:
                self.icon = 'heart' if self.icon == 'heart-outline' else 'heart-outline'

    ImageTouch:
        source: root.icon
        size_hint: None, None
        height: self.width
        pos_hint: {'center_x': .5}
        on_release: root.previous_dialog(icon=root.icon).open()

    MDLabel:
        font_style: 'Subtitle1'
        theme_text_color: 'Primary'
        text: 'Casio' + '\\n' + 'CVD-12L' + '\\n\\n' + '12 543 $'
        height: self.texture_size[1]
        halign: 'center'
        size_hint_y: None

    MDSeparator:

    MDFlatButton:
        text: 'To favorites'
        theme_text_color: 'Custom'
        text_color: app.theme_cls.primary_color
        pos_hint: {'center_x': .5}


<CardsBoxForShopWindow@BoxLayout>
    spacing: dp(10)
    product_image: ''
    product_image2: ''
    previous_dialog: None

    CardItemForShopWindow:
        icon: root.product_image
        previous_dialog: root.previous_dialog
    CardItemForShopWindow:
        icon: root.product_image2
        previous_dialog: root.previous_dialog


<CartScreen@BoxLayout>
    orientation: 'vertical'
    spacing: dp(5)
    padding: dp(5)

    MyRecycleView:
        id: rv_cart

    BoxLayout:
        size_hint_y: None
        height: self.minimum_height
        padding: dp(10)

        canvas.before:
            Color:
                rgba: 0, 0, 0, .1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [10,]

        MDFillRoundFlatButton
            text: 'Make a purchase'

        Widget:

        MDLabel:
            theme_text_color: 'Primary'
            font_style: 'Subtitle1'
            text: '1850 $'
            height: self.texture_size[1]
            size_hint_y: None
            pos_hint: {'center_y': .5}
            bold: True


<MainScreen@BoxLayout>
    orientation: 'vertical'

    BoxLayout:
        orientation: 'vertical'
        padding: dp(15)
        spacing: dp(10)

        canvas.before:
            Color:
                rgba:
                    1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint_y: None
            height: dp(48)
            spacing: dp(10)

            MDIconButton:
                icon: 'key-variant'

            MDLabel:
                font_style: 'H6'
                theme_text_color: 'Primary'
                halign: 'left'
                text: 'Registration'

        MDSeparator:

        Widget:
            size_hint_y: None
            height: dp(5)

        BoxLayout:
            spacing: dp(5)
            orientation: 'vertical'
            size_hint_y: None
            height: dp(48)

            MDTextField:
                size_hint: 1, None
                height: dp(48)
                hint_text: 'example@gmail.com'
                cursor_color: app.theme_cls.primary_color

        Widget:
            size_hint_y: None
            height: dp(5)

        MDLabel:
            markup: True

        Widget:
        Widget:
        Widget:

        BoxLayout:
            spacing: dp(2)
            size_hint_y: None
            height: dp(35)

            MDRaisedButton:
                text: 'Sign In'

            MDFlatButton:
                text: 'Sign Up'


<ShopWindow>
    name: 'shop window'
    on_enter:
        root.set_list_shop()
        root.set_list_cart()
        app.main_widget.ids.toolbar.title = 'Shop window'
        app.main_widget.ids.toolbar.right_action_items = []
    on_leave:
        root.set_chevron_back_screen()

    MDBottomNavigation:

        MDBottomNavigationItem:
            id: main
            name: 'main'
            text: 'Main'
            icon: 'home-variant'

            MainScreen:

        MDBottomNavigationItem:
            id: view_list
            name: 'view list'
            text: 'Catalog'
            icon: 'view-list'

            MyRecycleView:
                id: rv_main

        MDBottomNavigationItem:
            id: cart
            name: 'cart'
            text: 'Cart'
            icon: 'cart'

            CartScreen:
                id: cart_screen
'''


class ShopWindow(Screen):
    app = App.get_running_app()

    def set_list_shop(self):
        increment_left = -2
        for i in range(5):
            increment_left += 2
            self.app.main_widget.ids.scr_mngr.get_screen('shop window').ids.rv_main.data.append(
                {
                    'viewclass': 'CardsBoxForShopWindow',
                    'height': dp(300),
                    'product_image': './assets/clock-%d.png' % increment_left,
                    'product_image2': './assets/clock-%d.png' % (increment_left + 1),
                    'previous_dialog': dialog
                }
            )

    def set_menu_for_demo_apps(self):
        if not len(self.app.menu_for_demo_apps):
            for name_item in self.app.demo_apps_list:
                self.app.menu_for_demo_apps.append(
                    {'viewclass': 'OneLineListItem',
                     'text': name_item,
                     'on_release': lambda x=name_item: self.show_demo_apps(name_item)})

    def set_list_cart(self):
        for i in range(11):
            self.app.main_widget.ids.scr_mngr.get_screen(
                'shop window').ids.cart_screen.ids.rv_cart.data.append(
                    {
                        'viewclass': 'CardItemForCart',
                        'height': dp(150),
                        'product_image': './assets/clock-%d.png' % i
                    }
                )

    def show_demo_apps(self, name_item):
        self.app.main_widget.ids.scr_mngr.current = name_item.lower()
        self.app.instance_menu_demo_apps.dismiss()


class BaseDialog(ThemableBehavior, ModalView):
    canvas_color = ListProperty()
    callback = ObjectProperty(lambda x: None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas_color = self.theme_cls.primary_color
        self.canvas_color[3] = .75


class PreviousDialog(BaseDialog):
    icon = StringProperty()

    def on_open(self):
        print(111)
        Animation(size_hint=(.7, .7), d=.2, t='in_out_elastic').start(self)


dialog = PreviousDialog
