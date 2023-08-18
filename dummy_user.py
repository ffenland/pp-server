import faker
from django.contrib.auth import get_user_model

User = get_user_model()
fake = faker.Faker()


def create_dummy_users(num_users=50):
    for _ in range(num_users):
        User.objects.create(
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
            naver_id=fake.user_name(),
            kakao_id=fake.user_name(),
            avatar=fake.image_url(),
            license_number=fake.random_int(min=100000, max=999999),
            license_img=fake.image_url(),
            college=fake.word(),
            year_of_admission=fake.random_int(min=1900, max=2150),
            address_sgg_code=fake.random_int(min=10000, max=99999),
            address_sido=fake.city(),
            address_sgg=fake.city_suffix(),
        )


create_dummy_users()
