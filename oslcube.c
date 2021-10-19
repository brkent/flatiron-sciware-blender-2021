#include "stdosl.h"

shader volumeTexture(
    point Vector = P,
    string directory="//",
    string prefix="",
    int framePositions=3,
    string extension=".tif",
    float zMax = 2.0,
    int fromFrame = 1,
    int toFrame = 100,
    output color colorData = 1,
    output float nonColorData = 1,
)
{
    // Recenter the position around the object center to -1, 1 to 0, 1
    vector pos = 0.5 * (Vector + vector(1.0,1.0,1.0));

    // Calculate the image number
    int imageNum =  (int)floor((1.0 + toFrame - fromFrame) * (pos[2] / (zMax * 0.5)));
    int imageNum2 = (int)ceil((1.0 + toFrame - fromFrame) * (pos[2] / (zMax * 0.5)));
    float pixelFraction = mod((1.0 + toFrame - fromFrame) * pos[2] , (zMax * 0.5));

    // Make a format string from the given length (ie "%03d")
    string frameFormat = concat( "%0", format( "%d", framePositions ), "d" );
    // Format the current frame/image number (ie "003")
    string imageFrame = format( frameFormat, toFrame - imageNum );
    string imageFrame2 = format( frameFormat, toFrame - imageNum2 );
    // Make the full file name
    string fileName = concat( directory, prefix, imageFrame, extension );
    string fileName2 = concat( directory, prefix, imageFrame2, extension );

    // Get the color from the texture
    colorData    = texture3d( fileName, pos);
    float nonColorData1 = texture3d( fileName, pos);
    float nonColorData2 = texture3d( fileName2, pos);
    nonColorData = nonColorData1 * (1-pixelFraction) + nonColorData2*pixelFraction;
}