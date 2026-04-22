select
    service_type,
    service_type_name
from (
    values
        ('yellow_taxi', 'Yellow Taxi'),
        ('green_taxi', 'Green Taxi')
) as service_types(service_type, service_type_name)
