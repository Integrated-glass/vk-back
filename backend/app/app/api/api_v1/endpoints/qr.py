from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.utils.db import get_db
import os

from app.db_models.models import Volunteer
from app.crud.volunteer import get_by_id as get_volunteer_by_id
from app.api.utils.files import create_dir_if_not_exists

import qrcode as qr


qr_router = APIRouter()
qr_images_directory: str = os.getenv("QR_IMAGES_DIR", "./qr-img")
create_dir_if_not_exists(qr_images_directory)


@qr_router.get("/volunteer/{volunteer_id}")
def volunteer_id_qr(
  volunteer_id: int,
  db: Session = Depends(get_db)
):
  volunteer_id_qr_filename = "volunteer_id.png"
  volunteer_dir = qr_images_directory + "/" + str(volunteer_id)
  qr_path = volunteer_dir + "/" + volunteer_id_qr_filename

  if not os.path.exists(qr_path):
    create_dir_if_not_exists(volunteer_dir)
    volunteer: Volunteer = get_volunteer_by_id(db, volunteer_id)
    qr.make(data=volunteer.volunteer_id)\
      .save(qr_path)

  return {
    "image_uri": "/qr-img/" + str(volunteer_id) + "/" + volunteer_id_qr_filename
  }

# by volunteer id and event_id

