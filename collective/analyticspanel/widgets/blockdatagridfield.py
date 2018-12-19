# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield import (
    BlockDataGridField as BaseBlockField,
)
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer
from zope.schema.interfaces import IField


class BlockDataGridField(BaseBlockField):
    """ """

    auto_append = False


@adapter(IField, IFormLayer)
@implementer(IFieldWidget)
def BlockDataGridFieldFactory(field, request):
    """IFieldWidget factory for BlockDataGridField."""
    return FieldWidget(field, BlockDataGridField(request))
