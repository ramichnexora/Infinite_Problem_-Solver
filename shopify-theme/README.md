# Infinite Problem Solver - Shopify Theme

This directory contains Shopify Liquid sections for the Infinite Problem Solver store homepage.

## Integration Steps

### 1. Upload to Your Shopify Theme

1. Go to your Shopify Admin → **Online Store** → **Themes**
2. Find your active theme and click **Edit code**
3. In the code editor, navigate to the **Sections** folder
4. Click **Add a new section**
5. Name it `infinite-categories-section.liquid`
6. Copy the entire content from `sections/infinite-categories-section.liquid` and paste it into the editor
7. Click **Save**

### 2. Add the Section to Your Homepage

1. In Shopify Admin, go to **Online Store** → **Pages**
2. Click on your homepage (usually called "Home" or "Index")
3. In the page editor, click **Add section**
4. Find and select **"Infinite Problem Solver - Categories"**
5. The section will auto-populate with all 8 categories (Parenting, Business, Finance, Wellness, Relationships, Growth, Productivity, Technology)
6. Customize as needed:
   - Edit category titles, descriptions, and collection URLs
   - Upload images for each category (or leave empty to use emoji + gradient)
   - Adjust colors for gradients
   - Change emojis if desired
7. Click **Save**

### 3. Create Shopify Collections (If Not Already Created)

For each category, create a corresponding collection:
- `/collections/parenting`
- `/collections/business`
- `/collections/finance`
- `/collections/wellness`
- `/collections/relationships`
- `/collections/personal-growth`
- `/collections/productivity`
- `/collections/technology`

Or update the collection URLs in the section settings to match your existing collections.

## Features

- **Responsive Design**: Automatically adapts from mobile to desktop (280px min-width cards)
- **Category-Specific Colors**: Each category has a unique accent color on the top border
- **Flexible Images**: 
  - Upload real product/category images, or
  - Use emoji icons with gradient backgrounds as fallback
- **Dark Mode Support**: Automatically adapts to user's theme preference
- **Smooth Animations**: Hover effects with lift animation and image zoom
- **Accessibility**: Lazy loading, alt text, reduced motion support

## Customization

All 8 categories come pre-configured, but you can:
- Change titles and descriptions in the Shopify admin
- Upload category-specific images
- Adjust gradient colors using the Shopify color picker
- Update collection URLs to match your store structure
- Change emojis to different Unicode characters

## File Structure

```
shopify-theme/
└── sections/
    └── infinite-categories-section.liquid
```

## Technical Details

- **Template Engine**: Shopify Liquid
- **CSS**: Scoped within section using `{%- style -%}` tags
- **Grid Layout**: CSS Grid with `auto-fit` and `minmax()` for responsive columns
- **Image Optimization**: Shopify's native `img_url` filter for performance
- **Schema**: Fully configurable via Shopify admin with preset blocks
