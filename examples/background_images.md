# Background Images Example

This example demonstrates how to use background images and icons in blockdiag diagrams.

## Using Local Image Files

```
blockdiag {
    A [label = "Regular Node"];
    B [label = "", background = "/path/to/background.png"];
    C [icon = "/path/to/icon.png"];
    
    A -> B -> C;
}
```

## Using Remote URLs (requires network access)

```
blockdiag {
    // These nodes will have background images/icons if network access is available
    F [label = "", background = "http://example.com/_static/python-logo.gif"];
    G [label = "", background = "http://example.com/_static/python-logo.gif"];
    H [icon = "http://example.com/_static/help-browser.png"];
    I [icon = "http://example.com/_static/internet-mail.png"];
    
    F -> G -> H -> I;
}
```

## Configuration

By default, the extension will attempt to pre-fetch remote images before rendering.
This can be configured in your `mkdocs.yml`:

```yaml
markdown_extensions:
  - markdown_blockdiag:
      format: svg
      fetch_remote_images: true  # Enable prefetching (default)
```

### How It Works

1. **When `fetch_remote_images` is `true` (default)**:
   - The extension will attempt to download remote images referenced in `background` and `icon` attributes
   - Downloaded images are cached locally in temporary files
   - The diagram is rendered with the cached images
   - If download fails, the original URL is used (blockdiag will attempt to fetch)

2. **When `fetch_remote_images` is `false`**:
   - No pre-fetching occurs
   - blockdiag library will attempt to fetch images directly during rendering
   - May fail in restricted environments without network access

## Important Notes

- **Network Access**: Remote images require network access at build time
- **Local Files**: For offline builds, use local file paths instead of URLs
- **Security**: Be cautious when allowing remote image fetching from untrusted sources
- **Performance**: First render will be slower as images are downloaded; subsequent renders use cached images
- **Temporary Files**: Downloaded images are cached in temporary files. These are automatically cleaned up by the operating system, but very large numbers of images may consume disk space until cleanup occurs
- **File Size Limit**: Remote images are limited to 10 MB to prevent memory issues

## Troubleshooting

### Images Not Showing

If background images or icons are not appearing:

1. **Check network access**: Ensure your build environment can reach the remote URLs
2. **Verify URLs**: Make sure the image URLs are accessible and return valid image files
3. **Check format**: Supported formats include PNG, GIF, JPG
4. **Try local files**: For testing, use local file paths to rule out network issues
5. **Enable prefetching**: Ensure `fetch_remote_images: true` in your configuration

### Build Failures

If builds fail when using remote images:

1. Set `fetch_remote_images: false` to disable prefetching
2. Use local file paths instead of URLs
3. Check firewall/proxy settings that might block image downloads
