class MyFilterSet(FilterSet):
    negated_field__not = django_filters.NumberFilter(name='negated_field', exclude=True)

    class Meta:
        model = Model
        fields = ['some_field', 'some_other_field']