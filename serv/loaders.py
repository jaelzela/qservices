from serv.models import Category, Service, Review, Rate
import json
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))


def load_services():
    json_url = os.path.join(SITE_ROOT, 'static/json', 'g2crowd_apis.json')
    json_data = open(json_url)
    data = json.load(json_data)
    for api in data:
        try:
            categories = Category.objects.filter(category_name=api['category'])
        except KeyError:
            category = Category()
            category.category_id = 0
            categories = [category]

        if len(categories) > 0:
            save_service(api, categories[0].category_id)
        else:
            category = save_category(api)
            save_service(api, category.category_id)


def load_reviews():
    json_url = os.path.join(SITE_ROOT, 'static/json', 'g2crowd_reviews.json')
    json_data = open(json_url)
    data = json.load(json_data)
    for comment in data:
        services = Service.objects.filter(service_name=comment['api'])

        if len(services) > 0:
            save_review(comment, services[0].service_id)
        else:
            save_review(comment, 0)


def load_pweb_services():
    json_url = os.path.join(SITE_ROOT, 'static/json', 'pweb_apis.json')
    json_data = open(json_url)
    data = json.load(json_data)
    for api in data:
        try:
            categories = Category.objects.filter(category_name=api['category'].lower())
        except KeyError:
            category = Category()
            category.category_id = 0
            categories = [category]

        if len(categories) > 0:
            services = Service.objects.filter(service_name=api['name'])
            if len(services) > 0:
                services[0].description = api['description']
                services[0].category_id = categories[0].category_id
                services[0].save()
        else:
            category = save_category(api)
            services = Service.objects.filter(service_name=api['name'])
            if len(services) > 0:
                services[0].description = api['description']
                services[0].category_id = category.category_id
                services[0].save()


def load_pweb_reviews():
    json_url = os.path.join(SITE_ROOT, 'static/json', 'pweb_labeled_reviews.json')
    json_data = open(json_url)
    data = json.load(json_data)
    for comment in data:
        services = Service.objects.filter(service_name=comment['api'])

        if len(services) > 0:
            save_pweb_review(comment, services[0].service_id)
        else:
            service = save_service(dict({'name': comment['api'], 'description': ''}), 0)
            save_pweb_review(comment, service.service_id)


def save_service(api, category_id):
    service = Service()
    service.service_name = api['name']
    service.service_description = api['description']
    service.category_id = category_id
    service.save()
    return service


def save_category(api):
    category = Category()
    category.category_name = api['category']
    category.save()
    return category


def save_review(comment, service_id):
    if 'like' in comment:
        pos_review = Review()
        pos_review.service_id = service_id
        pos_review.review_text = comment['like']
        pos_review.review_date = comment['date']
        pos_review.review_polarity = 'pos'
        pos_review.save()

    if 'dislike' in comment:
        neg_review = Review()
        neg_review.service_id = service_id
        neg_review.review_text = comment['dislike']
        neg_review.review_date = comment['date']
        neg_review.review_polarity = 'neg'
        neg_review.save()


def save_pweb_review(comment, service_id):
    review = Review()
    review.service_id = service_id
    review.review_text = comment['review']
    review.review_polarity = comment['user_polarity']
    review.save()
    return review


def save_rates(rates, review_id):
    for user_rate in rates:
        rate = Rate()
        rate.review_id = review_id
        if user_rate > 0:
            rate.rate_polarity = 'pos'
        elif user_rate < 0:
            rate.rate_polarity = 'neg'
        else:
            rate.rate_polarity = 'neu'
