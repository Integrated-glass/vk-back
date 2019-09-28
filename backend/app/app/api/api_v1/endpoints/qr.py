from fastapi import APIRouter, Depends, Query, HTTPException
from starlette.status import HTTP_412_PRECONDITION_FAILED
from sqlalchemy.orm import Session
from app.api.utils.db import get_db
import os
import secrets
import json

from app.db_models.models import Volunteer, EventVolunteer, QR_data, ParticipationStatus
from app.crud.volunteer import get_by_id as get_volunteer_by_id
from app.crud.event_volunteer import get_by_event_id_volunteer_id
from app.api.utils.files import create_dir_if_not_exists

import qrcode as qr


qr_router = APIRouter()
qr_images_directory: str = os.getenv("QR_IMAGES_DIR", "./qr-img")
create_dir_if_not_exists(qr_images_directory)


@qr_router.get("/volunteer/{volunteer_id}")
def volunteer_id_qr(
  db: Session = Depends(get_db),
  *,
  volunteer_id: int,
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


@qr_router.get("/volunteer/{volunteer_id}/{event_id}")
def volunteer_event_qr(
  db: Session = Depends(get_db),
  *,
  need_regenerate: bool = Query(False),
  volunteer_id: int,
  event_id: int,
):
  qr_filename: str = f"{event_id}.png"
  qr_dir_path: str = qr_images_directory + "/" + str(volunteer_id)
  qr_file_path: str = qr_dir_path + "/" + qr_filename

  event_volunteer: EventVolunteer = get_by_event_id_volunteer_id(db, event_id, volunteer_id)

  if event_volunteer.participation_status == ParticipationStatus.APPROVED:
    if (not os.path.exists(qr_file_path)) or need_regenerate:
      create_dir_if_not_exists(qr_dir_path)
      new_qr_data: QR_data = QR_data(salt=secrets.token_urlsafe(16), event_volunteer_id=event_volunteer.id)
      db.add(new_qr_data)
      qr.make(data=json.dumps({
          "salt": new_qr_data.salt,
          "participation_id": str(event_volunteer.id),
        })
      )\
      .save(qr_file_path)

    return {
      "image_uri": "/qr-img/" + str(volunteer_id) + "/" + qr_filename
    }
  else:
    raise HTTPException(HTTP_412_PRECONDITION_FAILED, "The volunteer is not approved for the event.")
