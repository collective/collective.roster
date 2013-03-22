# -*- coding: utf-8 -*-

from five import grok
from zope.schema.interfaces import IInt
from z3c.form.widget import FieldWidget
from z3c.form.interfaces import IDataConverter
from z3c.form.browser.text import TextWidget
from z3c.form.converter import IntegerDataConverter


class ShortNumberWidget(TextWidget):
    """ Widget for displaying short numbers properly """


def ShortNumberFieldWidget(field, request):
    return FieldWidget(field, ShortNumberWidget(request))


class ShortNumberDataConverter(IntegerDataConverter, grok.MultiAdapter):
    grok.provides(IDataConverter)
    grok.adapts(IInt, ShortNumberWidget)

    def toWidgetValue(self, value):
        """ Adapts value to widget value without localized formatting """

        if value is self.field.missing_value:
            return u''

        return unicode(value)
