from django.core.management.base import BaseCommand
from django_apps.foods.models import Unit, UnitConversion


class Command(BaseCommand):
    help = 'Calculates conversions based on grams to all other units.'

    def handle(self, *args, **options):
        # This command populates the foods_unit_conversions table in the db.
        # Prereqs: must have all conversions from grams to all other units in
        # UnitConversions table.

        all_units = Unit.objects.all()
        gram = Unit.objects.get(name='gram')
        existing_unit_conversions = UnitConversion.objects.all()

        # Make sure unit conversions for grams to all other units exist:
        for unit in all_units:
            # Skip if unit is gram.
            if unit == gram:
                continue
            if not existing_unit_conversions.filter(
                    from_unit=gram, to_unit=unit).exists():
                return self.stdout.write(self.style.ERROR(
                    'Failed to update conversions: please make \
                    sure unit conversions exist from grams to \
                    all other units before running this command'))

        # Step 1. Get conversions for all units to grams
        for unit in all_units:
            # Skip if unit is gram.
            if unit == gram:
                continue
            # Skip if conversion record exists.
            if existing_unit_conversions.filter(
                    from_unit=unit, to_unit=gram).exists():
                continue
            from_grams = existing_unit_conversions.filter(
                from_unit=gram, to_unit=unit)[0]
            to_grams_coefficient = 1/from_grams.qty_conversion_coefficient
            to_grams = UnitConversion(
                from_unit=unit,
                to_unit=gram,
                qty_conversion_coefficient=to_grams_coefficient
            )
            # Could bulk save but don't care about efficiency for this one.
            to_grams.save()

        # Step 2. Find all possible conversions:
        # Refresh existing unit conversions:
        existing_unit_conversions = UnitConversion.objects.all()
        for from_unit in all_units:
            for to_unit in all_units:
                # Skip if units are equal.
                if from_unit == to_unit:
                    continue
                # Skip if conversion record exists.
                if existing_unit_conversions.filter(
                        from_unit=from_unit, to_unit=to_unit).exists():
                    continue
                # Convert to grams
                qty_grams = existing_unit_conversions.filter(
                    from_unit=from_unit, to_unit=gram
                )[0].qty_conversion_coefficient

                # Convert to to_unit
                from_gram_qty_coefficient = existing_unit_conversions.filter(
                    from_unit=gram, to_unit=to_unit
                )[0].qty_conversion_coefficient

                qty_to_unit = qty_grams * from_gram_qty_coefficient
                from_to_qty_coefficient = UnitConversion(
                    from_unit=from_unit,
                    to_unit=to_unit,
                    qty_conversion_coefficient=qty_to_unit
                )
                # Could bulk save but don't care about efficiency for this one.
                from_to_qty_coefficient.save()

        self.stdout.write(self.style.SUCCESS(
            'Successfully updated conversions!'))
