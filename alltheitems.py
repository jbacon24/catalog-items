from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Beauty, Base, BeautyItem, User

engine = create_engine('sqlite:///beautyitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
User1 = User(username="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Items for Makeup
product1 = Beauty(user_id=1, name="Makeup")

session.add(product1)
session.commit()

beautyItem1 = BeautyItem(user_id=1, name="Eye Shadow", description="Cosmetic applied to the eyelid to create depth and dimension",
                     price="$7.50", feature="eyes", product=product1)

session.add(beautyItem1)
session.commit()


beautyItem2 = BeautyItem(user_id=1, name="Lip Gloss", description="Product used to provide a glossy shine and mild color to the lips",
                     price="$2.99", feature="lips", product=product1)

session.add(beautyItem2)
session.commit()

beautyItem3 = BeautyItem(user_id=1, name="Mascara", description="Makeup used to enhance the eyelashes",
                     price="$5.50", feature="eyes", product=product1)

session.add(beautyItem3)
session.commit()

beautyItem4 = BeautyItem(user_id=1, name="Eyeliner", description="Makeup used to emphasize the eyelids and accent the shape of eyes",
                     price="$3.99", feature="eyes", product=product1)

session.add(beautyItem4)
session.commit()

beautyItem5 = BeautyItem(user_id=1, name="Foundation", description="Makeup applied to the face to create an even complexion",
                     price="$7.99", feature="face", product=product1)

session.add(beautyItem5)
session.commit()

beautyItem6 = BeautyItem(user_id=1, name="Blush", description="Makeup applied to the cheeks to add a subtle redness",
                     price="$5.99", feature="face", product=product1)

session.add(beautyItem6)
session.commit()

beautyItem7 = BeautyItem(user_id=1, name="Highlighter", description="Used for contouring, makeup that reflects light and brightens the skin on the applied area",
                     price="$4.99", feature="face", product=product1)

session.add(beautyItem7)
session.commit()

beautyItem8 = BeautyItem(user_id=1, name="Concealer", description="Color correcting makeup used to cover up blemishes, dark spots, aging spots, etc.",
                     price="$3.49", feature="face", product=product1)

session.add(beautyItem8)
session.commit()

beautyItem9 = BeautyItem(user_id=1, name="Primer", description="Base for foundation that allows foundation to appear smoother and last longer",
                     price="$10.99", feature="face", product=product1)

session.add(beautyItem9)
session.commit()


# Items for Skincare
product2 = Beauty(user_id=1, name="Skincare")

session.add(product2)
session.commit()


beautyItem1 = BeautyItem(user_id=1, name="Masks", description="Product used to cleanse, unclog pores, and improve skin appearance",
                     price="$7.99", feature="face", product=product2)

session.add(beautyItem1)
session.commit()

beautyItem2 = BeautyItem(user_id=1,
    name="Makeup Wipes", description="Product used to remove makeup and clean the face", price="$25", feature="Entree", product=product2)

session.add(beautyItem2)
session.commit()

beautyItem3 = BeautyItem(user_id=1, name="Cleansers", description="Facial care product used to remove makeup and other pollutants from the skin",
                     price="15", feature="face", product=product2)

session.add(beautyItem3)
session.commit()

beautyItem4 = BeautyItem(user_id=1, name="Sunscreen", description="Lotion or spray used to protect the skin from UV rays and reduce sunburn",
                     price="12", feature="face", product=product2)

session.add(beautyItem4)
session.commit()

beautyItem5 = BeautyItem(user_id=1, name="Moisturizer", description="Product used to hyradte skin",
                     price="14", feature="face", product=product2)

session.add(beautyItem5)
session.commit()


# Items for Haircare
product3 = Beauty(user_id=1, name="Haircare")

session.add(product3)
session.commit()


beautyItem1 = BeautyItem(user_id=1, name="Shampoo", description="Product used to remove surface debris from scalp and hair",
                     price="$8.99", feature="hair", product=product3)

session.add(beautyItem1)
session.commit()

beautyItem2 = BeautyItem(user_id=1, name="Conditioner", description="Product used to improve the feel and appearance of hair and helps to detangle strands",
                     price="$6.99", feature="hair", product=product3)

session.add(beautyItem2)
session.commit()

beautyItem3 = BeautyItem(user_id=1, name="Hair Spray", description="Styling product used to protect against humity and hold hair in place",
                     price="$9.95", feature="hair", product=product3)

session.add(beautyItem3)
session.commit()

beautyItem4 = BeautyItem(user_id=1, name="Hair Masks", description="Hair treatment to deeply hydrate and nurture hair",
                     price="$6.99", feature="hair", product=product3)

session.add(beautyItem4)
session.commit()


# Items for Bath&Body
product4 = Beauty(user_id=1, name="Bath&Body")

session.add(product4)
session.commit()


beautyItem1 = BeautyItem(user_id=1, name="Exfoliator", description="Product used to remove dead skin cells",
                     price="$2.99", feature="body", product=product4)

session.add(beautyItem1)
session.commit()

beautyItem2 = BeautyItem(user_id=1, name="Body Wash", description="Cleasners used to remove dirt, oil, and other debris from the skin",
                     price="$5.99", feature="body", product=product4)

session.add(beautyItem2)
session.commit()

beautyItem3 = BeautyItem(user_id=1, name="Lotion", description="Product used to smooth and moisturize the skin",
                     price="$4.50", feature="body", product=product4)

session.add(beautyItem3)
session.commit()

beautyItem4 = BeautyItem(user_id=1, name="Deodorant", description="Product used to mask body odor and prevent sweating",
                     price="$6.95", feature="body", product=product4)

session.add(beautyItem4)
session.commit()


print("added beauty products!")
