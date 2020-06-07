from actualPlanner.models import Rating

def basicTable():
    all_data = Rating.objects.all().values()
    
    pass