import io
import base64
import qrcode
from qrcode.image.styledpil import StyledPilImage

def generate_khqr_qr_code(amount: float, merchant_name: str = "WATCH SHOP", order_number: str = "") -> str:
    """
    Generates a KHQR (Bakong / KHQR standard format) QR code and returns
    it as a base64 Data URL image string.
    """
    amount_str = f"{amount:.2f}"
    # Formulate Bakong/KHQR-compatible mock EMVCo payload
    payload = (
        f"000201010212"
        f"29370016bakong@nbc.org.kh0113watch_shop_kh"
        f"52045999"
        f"5303840"
        f"54{len(amount_str):02d}{amount_str}"
        f"5802KH"
        f"59{len(merchant_name):02d}{merchant_name}"
        f"6010PHNOM PENH"
        f"62{len(order_number):02d}{order_number}"
        f"6304ABCD"
    )

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=3,
    )
    qr.add_data(payload)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#1e293b", back_color="#ffffff")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"
