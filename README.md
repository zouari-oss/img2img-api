[![Contributors](https://img.shields.io/badge/CONTRIBUTORS-01-blue?style=plastic)](https://github.com/zouari-oss/img2img-api/graphs/contributors)
[![Forks](https://img.shields.io/badge/FORKS-00-blue?style=plastic)](https://github.com/zouari-oss/img2img-api/network/members)
[![Stargazers](https://img.shields.io/badge/STARS-01-blue?style=plastic)](https://github.com/zouari-oss/img2img-api/stargazers)
[![Issues](https://img.shields.io/badge/ISSUES-00-blue?style=plastic)](https://github.com/zouari-oss/img2img-api/issues)
[![GPL3.0 License](https://img.shields.io/badge/LICENSE-GPL3.0-blue?style=plastic)](https://raw.githubusercontent.com/zouari-oss/img2img-api/refs/heads/main/LICENSE)
[![Linkedin](https://img.shields.io/badge/Linkedin-7k-blue?style=plastic)](https://www.linkedin.com/in/zouari-omar)

<div align="center">
  <a href="https://github.com/zouari-oss/img2img-api">
    <img src="https://github.com/zouari-oss/img2img-api/raw/main/res/img/logo.png" alt="img2img-api.png" width="300">
  </a>
  <h1>img2img-api</h1>
  <h6>Generate images from input images + prompts using Stable Diffusion (Anything V5)</h6>
  <br />
</div>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#api-example">API Example</a> •
  <a href="#usage">Usage</a> •
  <a href="#download">Download</a> •
  <a href="#emailware">Emailware</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a> •
  <a href="#contact">Contact</a> •
  <a href="#acknowledgments">Acknowledgments</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-Web%20Framework-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white"/>
  <img src="https://img.shields.io/badge/Torch-ML%20Framework-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Safetensors-Model%20Format-blueviolet?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/AnythingV5-Stable%20Diffusion%20Model-8A2BE2?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Machine%20Learning-AI-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/API-RESTful-informational?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Open%20Source-Yes-3DA639?style=for-the-badge&logo=opensourceinitiative&logoColor=white"/>
</p>

![screenshot](https://github.com/zouari-oss/img2img-api/raw/main/res/img/screenshot.png)

## Overview

**img2img-api** exposes a simple HTTP API to generate images from an input image plus text prompts using Stable Diffusion (model: Anything V5). It accepts an initial URL image with generation parameters and returns generated images as URL.

## Key Features

- **FastAPI HTTP API** with OpenAPI docs available at `/docs`
- Img2Img generation using **Stable Diffusion** (Anything V5) via diffusers' StableDiffusionImg2ImgPipeline
- Accepts an image URL (HTTP/HTTPS); server downloads the input image for processing
- Generated images are uploaded to a configured host and the API returns the hosted image URL
- Configurable via environment variables: `MODEL_PATH`, `DEVICE`, `FREEIMAGE_API_KEY`, `FREEIMAGE_UPLOAD_URL`
- **GPU support (CUDA)** with automatic float16 when available; attention slicing enabled for memory efficiency
- Request validation with **Pydantic** schemas and clear JSON responses on success/error
- **CORS enabled** for browser-based clients; small, dependency-light service suitable for local or server use

## API Example

```http
POST /api/generate
Content-Type: application/json
```

This project expects a JSON body with an image_url pointing to a publicly-accessible image. The server will download that image, run img2img using the configured Stable Diffusion model, upload the result to the configured free image host, and return the hosted URL.

Request (JSON example):

```json
{
  "image_url": "https://example.com/input.jpg",
  "prompt": "A fantasy landscape painting, vibrant colors, highly detailed",
  "negative_prompt": "lowres, blurry"
}
```

Response (JSON example):

```json
{
  "status": "success",
  "image_url": "https://freeimage.host/abcd1234.png"
}
```

> [!NOTE]
>
> - `image_url` must be an HTTP(S) URL reachable by the server (no local file paths or data URLs).
> - The service requires `FREEIMAGE_API_KEY` and `FREEIMAGE_UPLOAD_URL` to be configured so the generated image can be uploaded and hosted.

## Usage

Run locally (development):

```bash
git clone https://github.com/zouari-oss/img2img-api && cd img2img-api/project
chmod u+x setup && ./setup
fastapi run
```

> [!IMPORTANT]
> Base URL (local): <http://localhost:8000>

### curl (JSON with image_url)

```bash
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url":"https://example.com/input.jpg",
    "prompt":"A photorealistic portrait of a golden retriever",
    "negative_prompt":"lowres, blurry"
  }'
```

### JavaScript (fetch, Node/browser)

```javascript
fetch("http://localhost:8000/api/generate", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    image_url: "https://example.com/input.jpg",
    prompt: "A dreamy landscape",
    negative_prompt: "",
  }),
})
  .then((res) => res.json())
  .then((data) => console.log("Hosted URL:", data.image_url))
  .catch(console.error);
```

### PHP (curl)

```php
<?php
$ch = curl_init("http://localhost:8000/api/generate");
$data = json_encode([
  "image_url" => "https://example.com/input.jpg",
  "prompt" => "A watercolor painting of mountains",
  "negative_prompt" => ""
]);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
curl_close($ch);
var_dump(json_decode($response, true));
?>
```

### Java (HttpURLConnection)

```java
URL url = new URL("http://localhost:8000/api/generate");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("POST");
conn.setRequestProperty("Content-Type", "application/json");
conn.setDoOutput(true);
String jsonInputString = "{\"image_url\":\"https://example.com/input.jpg\",\"prompt\":\"A surreal landscape\",\"negative_prompt\":\"\"}";
try(OutputStream os = conn.getOutputStream()) {
  byte[] input = jsonInputString.getBytes("utf-8");
  os.write(input, 0, input.length);
}
try(BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "utf-8"))) {
  StringBuilder response = new StringBuilder();
  String responseLine;
  while ((responseLine = br.readLine()) != null) {
    response.append(responseLine.trim());
  }
  System.out.println(response.toString());
}
```

### C (libcurl)

```c
#include <stdio.h>
#include <curl/curl.h>
int main(void){
  CURL *curl = curl_easy_init();
  if(curl) {
    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    const char *data = "{\"image_url\":\"https://example.com/input.jpg\",\"prompt\":\"A cinematic cityscape\",\"negative_prompt\":\"\"}";
    curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:8000/api/generate");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);
    CURLcode res = curl_easy_perform(curl);
    if(res != CURLE_OK) fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);
  }
  return 0;
}
```

## Download

You can [download](https://github.com/zouari-oss/img2img-api/releases) the latest installable version of img2img-api for Windows, macOS and Linux.

## Emailware

img2img-api is an emailware. Meaning, if you liked using this app or it has helped you in any way,
would like you send as an email at <zouariomar20@gmail.com> about anything you'd want to say about
this software. I'd really appreciate it!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This repository is licensed under the **GPL-3.0 License**. You are free to use, modify, and distribute the content. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, feel free to reach out:

- **GitHub**: [zouari-oss](https://github.com/zouari-oss)
- **Email**: <zouariomar20@gmail.com>
- **LinkedIn**: [zouari-omar](https://www.linkedin.com/in/zouari-omar)

## Acknowledgments

Built with ❤️ for the open-source community.
