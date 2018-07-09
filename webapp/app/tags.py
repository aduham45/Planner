class Tags:
    def __init__(self, items):
        self.items = items
    def __iter__(self):
        for item in self.items:
            yield(item)


TAGS = [('Track','Track'),('Service','Service'),('Boutique','Boutique'),('Boxing','Boxing'),('Theme','Theme'),('Station','Station'),('Playground','Playground'),\
        ('Hobby','Hobby'),('Fitness','Fitness'),('Comedy','Comedy'),('Public','Public'),('Bookste','Bookste'),('Bistro','Bistro'),('Ballroom','Ballroom'),\
        ('Gym','Gym'),('Football','Football'),('Cultural','Cultural'),('French','French'),('Joint','Joint'),('Liqu','Liqu'),('Studio','Studio'),('Aquarium','Aquarium'),\
        ('Marina','Marina'),('Karaoke','Karaoke'),('Pool','Pool'),('Furniture','Furniture'),('Building','Building'),('Skating','Skating'),('Agency','Agency'),\
        ('Bar','Bar'),('Restaurant','Restaurant'),('Venue','Venue'),('Bakery','Bakery'),('Farmers','Farmers'),('Nightlife','Nightlife'),('Bowling','Bowling'),\
        ('Landmark','Landmark'),('Ferry','Ferry'),('Athletics','Athletics'),('Non-Profit','Non-Profit'),('Wine','Wine'),('Shop','Shop'),('Dojo','Dojo'),('Art','Art'),\
        ('Indie','Indie'),('Rest','Rest'),('Gallery','Gallery'),('Planetarium','Planetarium'),('Tag','Tag'),('Rink','Rink'),('Go','Go'),('Spa','Spa'),\
        ('Outdo','Outdo'),('Event','Event'),('Arts','Arts'),('Cowking','Cowking'),('Jewelry','Jewelry'),('Arcade','Arcade'),('Entertainment','Entertainment'),\
        ('Museum','Museum'),('Zoo','Zoo'),('Beer','Beer'),('Alley','Alley'),('Stationery','Stationery'),('Diner','Diner'),('Coffee','Coffee'),('Run','Run'),\
        ('Fountain','Fountain'),('Park','Park'),('Miscellaneous','Miscellaneous'),('Pub','Pub'),('Water','Water'),('Fest','Fest'),('Salsa','Salsa'),('Perfming','Perfming'),\
        ('Ride','Ride'),('Arena','Arena'),('Palace','Palace'),('School','School'),('Theater','Theater'),('Gaming','Gaming'),('Scenic','Scenic'),('Tapas','Tapas'),\
        ('Plaza','Plaza'),('Racetrack','Racetrack'),('Tour','Tour'),('Rock','Rock'),('Recding','Recding'),('Gay','Gay'),('Reservoir','Reservoir'),('Dance','Dance'),\
        ('Fish','Fish'),('Circus','Circus'),('Harb','Harb'),('Amphitheater','Amphitheater'),('Auditium','Auditium'),('Facty','Facty'),('Design','Design'),('Market','Market'),\
        ('Home','Home'),('Cafe','Cafe'),('Photography','Photography'),('Travel','Travel'),('Castle','Castle'),('Lounge','Lounge'),('Music','Music'),('Cosmetics','Cosmetics'),\
        ('Stadium','Stadium'),('Provider','Provider'),('Piano','Piano'),('Meeting','Meeting'),('Temple','Temple'),('Lookout','Lookout'),('Used','Used'),('Cocktail','Cocktail'),\
        ('Farm','Farm'),('Hotel','Hotel'),('Baseball','Baseball'),('Botanical','Botanical'),('Histy','Histy'),('Ste','Ste'),('Laser','Laser'),('Center','Center'),\
        ('Motcycle','Motcycle'),('Mini','Mini'),('Opera','Opera'),('Science','Science'),('Casino','Casino'),('Volleyball','Volleyball'),('American','American'),\
        ('Histic','Histic'),('Sculpture','Sculpture'),('BBQ','BBQ'),('Memial','Memial'),('Golf','Golf'),('Concert','Concert'),('Office','Office'),('Field','Field'),\
        ('House','House'),('Library','Library'),('General','General'),('Martial','Martial'),('College','College'),('Roller','Roller'),('Church','Church'),('Spts','Spts'),\
        ('Boat','Boat'),('Hockey','Hockey'),('City','City'),('Racecourse','Racecourse'),('Basketball','Basketball'),('Court','Court'),('Space','Space'),('Movie','Movie'),\
        ('Tennis','Tennis'),('Cemetery','Cemetery'),('Attraction','Attraction'),('Other','Other'),('Convention','Convention'),('Soccer','Soccer'),('Beach','Beach'),\
        ('Brewery','Brewery'),('Stables','Stables'),('Garden','Garden'),('Pedestrian','Pedestrian'),('Outdos','Outdos'),('Exhibit','Exhibit'),('Crafts','Crafts'),\
        ('Jazz','Jazz'),('Lab','Lab'),('Skate','Skate'),('Flea','Flea'),('Rental','Rental'),('Hall','Hall'),('Great','Great'),('Rugby','Rugby'),('Room','Room'),\
        ('Medical','Medical'),('Village','Village'),('Dog','Dog'),('Nightclub','Nightclub'),('Winery','Winery'),('Monument','Monument'),('Neighbhood','Neighbhood'),\
        ('Bridge','Bridge'),('Kart','Kart'),('Site','Site'),('Club','Club'),('Street','Street'),('Radio','Radio'),('Multiplex','Multiplex'),('Pitch','Pitch'),('Clothing','Clothing')]


