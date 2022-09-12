Unreleased
----------

    See on GitHub: `branch master <https://github.com/kivymd/KivyMD/tree/master>`_ | `compare 1.0.2/master <https://github.com/kivymd/KivyMD/compare/1.0.2...master>`_

    .. code-block:: bash

       pip install https://github.com/kivymd/KivyMD/archive/master.zip

* Bug fixes and other minor improvements.
* Add `closing_interval <https://kivymd.readthedocs.io/en/latest/components/card/#kivymd.uix.card.card.MDCardSwipe.closing_interval>`_ parameter to `MDCardSwipe <https://kivymd.readthedocs.io/en/latest/components/card/#kivymd.uix.card.card.MDCardSwipe>`_ class.
* Add implementation of elevation behavior on shaders.
* Add `validator <https://kivymd.readthedocs.io/en/latest/components/textfield/#kivymd.uix.textfield.textfield.MDTextField.validator>`_ property to `MDTextField <https://kivymd.readthedocs.io/en/latest/components/textfield/#kivymd.uix.textfield.textfield.MDTextFieldR>`_ class: the type of text field for entering Email, time, etc. Automatically sets the type of the text field as `error` if the user input does not match any of the set validation types.
* Add `theme_style_switch_animation <https://kivymd.readthedocs.io/en/latest/themes/theming/#kivymd.theming.ThemeManager.theme_style_switch_animation>`_ property to animate the colors of the application when switching the color scheme of the application `('Dark/light')`.
* Add `theme_style_switch_animation_duration <https://kivymd.readthedocs.io/en/latest/themes/theming/#kivymd.theming.ThemeManager.theme_style_switch_animation_duration>`_ property to duration of the animation of switching the color scheme of the application `("Dark/ light")`.
* `Fix <https://github.com/kivymd/KivyMD/issues/1332>`_ memory leak when dynamically adding and removing `KivyMD` widgets.
* `Fix <https://github.com/kivymd/KivyMD/pull/1344>`_ `MDBottomNavigation <https://kivymd.readthedocs.io/en/latest/components/bottomnavigation/>`_ slide transition direction.