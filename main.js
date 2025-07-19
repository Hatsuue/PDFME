const rekeningData = {
  seabank: { name: "Sea Bank", number: "9016 9922 2256" },
  bca: { name: "BCA Virtual", number: "3901 0859 1028 57730" },
  bri: { name: "BRI Virtual", number: "8881 0859 1028 57730" },
  mandiri: { name: "Mandiri Virtual", number: "89508 59028 57730" },
  bni: { name: "BNI Virtual", number: "881 0859 1028 57730" },
  ovo: { name: "OVO", number: "0859 1028 57730" },
  gopay: { name: "GoPay", number: "0859 1028 57730" },
  dana: { name: "DANA", number: "0859 1028 57730" },
  shopeepay: { name: "ShopeePay", number: "0859 1028 57730" }
};
const rekeningSelect = document.getElementById('rekening');
const rekeningInfo = document.getElementById('rekening-info');
const rekeningName = rekeningInfo ? rekeningInfo.querySelector('h2') : null;
const rekeningNumber = document.getElementById('rekening-number');
const copyBtn = document.getElementById('copyBtn');
if (rekeningSelect && rekeningName && rekeningNumber && copyBtn) {
  rekeningSelect.addEventListener('change', function() {
    const selected = rekeningSelect.value;
    rekeningName.textContent = rekeningData[selected].name;
    rekeningNumber.textContent = rekeningData[selected].number;
  });
  copyBtn.onclick = function() {
    const selected = rekeningSelect.value;
    const rekening = rekeningData[selected].number;
    navigator.clipboard.writeText(rekening).then(function() {
      alert("Nomor rekening disalin!");
    });
  };
}
// Preview gambar otomatis saat user pilih file
const imageInput = document.getElementById('image-upload');
const imagePreview = document.getElementById('image-preview');

if (imageInput && imagePreview) {
  imageInput.addEventListener('change', function() {
    imagePreview.innerHTML = ""; // Clear preview
    const file = this.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = function(e) {
        imagePreview.innerHTML = `<img src="${e.target.result}" style="max-width:180px;max-height:180px;border-radius:8px;box-shadow:0 2px 8px #0001;">`;
      };
      reader.readAsDataURL(file);
    }
  });
}