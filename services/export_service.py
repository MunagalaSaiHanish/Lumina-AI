from io import BytesIO
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)
from reportlab.lib.units import inch


def generate_pdf(
    metadata,
    summary,
    takeaways,
    topics
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER

    heading = styles["Heading2"]

    normal = styles["BodyText"]

    story = []

    #title

    story.append(
        Paragraph(
            "AI Summary",
            title_style
        )
    )

    story.append(
        Spacer(1, 0.3 * inch)
    )

    #video information

    story.append(
        Paragraph(
            f"<b>Video Title:</b> {metadata['title']}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Channel:</b> {metadata['channel']}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>YouTube URL:</b> {metadata['url']}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated On:</b> {datetime.now().strftime('%d %b %Y %I:%M %p')}",
            normal
        )
    )

    story.append(
        Spacer(1, 0.3 * inch)
    )

    #summary

    story.append(
        Paragraph(
            "AI Summary",
            heading
        )
    )

    story.append(
        Paragraph(
            summary.replace("\n", "<br/>"),
            normal
        )
    )

    story.append(
        Spacer(1, 0.3 * inch)
    )

    #takeaways

    story.append(
        Paragraph(
            "Key Takeaways",
            heading
        )
    )

    takeaway_items = []

    for takeaway in takeaways:

        takeaway_items.append(
            ListItem(
                Paragraph(
                    takeaway,
                    normal
                )
            )
        )

    story.append(
        ListFlowable(
            takeaway_items,
            bulletType="bullet"
        )
    )

    story.append(
        Spacer(1, 0.3 * inch)
    )

    #topics

    story.append(
        Paragraph(
            "Main Topics",
            heading
        )
    )

    topic_items = []

    for topic in topics:

        topic_items.append(
            ListItem(
                Paragraph(
                    topic,
                    normal
                )
            )
        )

    story.append(
        ListFlowable(
            topic_items,
            bulletType="bullet"
        )
    )

    story.append(
        Spacer(1, 0.5 * inch)
    )

    #footer

    story.append(
        Paragraph(
            "<b>Powered by Lumina AI</b>",
            title_style
        )
    )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf