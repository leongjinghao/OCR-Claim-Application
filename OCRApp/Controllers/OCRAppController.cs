using Microsoft.AspNetCore.Mvc;
using Python.Runtime;

[Route("api/[controller]")]
[ApiController]
public class OCRAppController : ControllerBase
{
    [HttpPost("")]
    public IActionResult Post(IFormFile imageFile)
    {
        // initialise Pythonnet engine
        if (!PythonEngine.IsInitialized)
        {
            Runtime.PythonDLL = @"C:\Users\leong\AppData\Local\Programs\Python\Python39\python39.dll";
            PythonEngine.Initialize();
	        PythonEngine.BeginAllowThreads();
        }

        // Acquire the Python Global Interpreter Lock (GIL)
        using (Py.GIL())
        {
            dynamic sys = Py.Import("sys");
            sys.path.append("Scripts");

            dynamic OCRAppScript = Py.Import("OCRApp");
            
            byte[] imageBytes;
            using (var memoryStream = new MemoryStream())
            {
                imageFile.CopyTo(memoryStream);
                imageBytes = memoryStream.ToArray();
            }

            var result = OCRAppScript.OCRApp(imageBytes);

            return Ok(result.ToString());
        }
    }
}