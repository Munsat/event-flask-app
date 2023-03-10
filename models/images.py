from database import sql_multiple_write, sql_select_all_by_col

class Image:
    def __init__(self, id, public_id, image_url, event_id) -> None:
        self.id=id
        self.public_id = public_id
        self.image_url = image_url
        self.event_id = event_id

def insert_image(image_rows):
    return sql_multiple_write('INSERT INTO images (public_id, image_url, event_id) VALUES %s', image_rows)

def show_images(event_id):
    images = sql_select_all_by_col('SELECT id, public_id, image_url, event_id FROM images WHERE event_id = %s', [event_id])
    image_list = []
    for image in images:
        image_list.append(Image(id=image['id'],
                          public_id=image['public_id'],
                          image_url=image['image_url'],
                          event_id=image['event_id']))
    return image_list    



