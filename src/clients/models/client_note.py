from django.db import models

from .base import BaseModel

ch_note_type = (
    ("note", "Note"),
    ("follow_up", "Follow Up"),
    ("do_not_mention", "Do Not Mention"),
    ("preferences", "Preferences"),
    ("archive", "Archive"),
)


class ClientNote(BaseModel):
    """
    Class descriptor
    """

    client_id_fk = models.ForeignKey(
        "ClientDetail", on_delete=models.CASCADE, related_name="notes"
    )

    title = models.CharField("Note Title", max_length=100)
    body = models.CharField("Note", max_length=2000)
    note_type = models.CharField(
        "Note Type", max_length=50, choices=ch_note_type, default="Note"
    )

    def __str__(self):
        return self.title
