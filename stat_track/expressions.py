from django.db.models import F, ExpressionWrapper, FloatField, Case, Value, When, IntegerField
from django.db.models.functions import Round

# Query expression
winrate_expression = ExpressionWrapper(
    Case(
        When(match_count=0, then=Value(50.0)),
        default=Round(((F('wins') + (F('draws') / 3.0)) / F('match_count')) * 100.0),
        output_field=IntegerField()
    ),
    output_field=IntegerField()
)


goals_per_match_expression = ExpressionWrapper(
    Case(
        When(match_count=0, then=Value(0.0)),
        default=Round((F('goals') / 1.0) / F('match_count'), precision=2),
        output_field=FloatField()
    ),
    output_field=FloatField()
)

points_per_match_expression = ExpressionWrapper(
    Case(
        When(match_count=0, then=Value(0)),
        default=Round((F('points') / 1.0)/ F('match_count'), precision=2),
        output_field=FloatField()
    ),
    output_field=FloatField()
)
