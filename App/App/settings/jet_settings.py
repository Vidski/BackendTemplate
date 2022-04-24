from django.utils.html import format_html


"""
JET Documentation: https://django-jet-reboot.readthedocs.io/
"""

JET_SIDE_MENU_COMPACT = True
JET_THEMES = [
    {
        'theme': 'default',  # theme folder name
        'color': '#47bac1',  # color of the theme's button in user menu
        'title': 'Default',  # theme title
    },
    {'theme': 'green', 'color': '#44b78b', 'title': 'Green'},
    {'theme': 'light-green', 'color': '#2faa60', 'title': 'Light Green'},
    {'theme': 'light-violet', 'color': '#a464c4', 'title': 'Light Violet'},
    {'theme': 'light-blue', 'color': '#5EADDE', 'title': 'Light Blue'},
    {'theme': 'light-gray', 'color': '#222', 'title': 'Light Gray'},
]

icon_dimensions = 'width="14px" height="14px"'
color = 'white'
icon_color = f'style="fill: {color}"'

user_label_with_icon = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" '
    + f'{icon_dimensions}><path d="M224 256c70.7 0 128-57.31 128-128s-57.3-128-'
    + '128-128C153.3 0 96 57.31 96 128S153.3 256 224 256zM274.7 304H173.3C77.61'
    + ' 304 0 381.6 0 477.3c0 19.14 15.52 34.67 34.66 34.67h378.7C432.5 512 448'
    + f' 496.5 448 477.3C448 381.6 370.4 304 274.7 304z"{icon_color}/></svg>&n'
    + 'bsp;&nbsp;&nbsp;Users'
)

profile_label_with_icon = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"'
    + f'{icon_dimensions}><path d="M512 32H64C28.65 32 0 60.65 0 96v320c0 35.35'
    + ' 28.65 64 64 64h448c35.35 0 64-28.65 64-64V96C576 60.65 547.3 32 512 32z'
    + 'M176 128c35.35 0 64 28.65 64 64s-28.65 64-64 64s-64-28.65-64-64S140.7 12'
    + '8 176 128zM272 384h-192C71.16 384 64 376.8 64 368C64 323.8 99.82 288 144'
    + ' 288h64c44.18 0 80 35.82 80 80C288 376.8 280.8 384 272 384zM496 320h-128'
    + 'C359.2 320 352 312.8 352 304S359.2 288 368 288h128C504.8 288 512 295.2 5'
    + '12 304S504.8 320 496 320zM496 256h-128C359.2 256 352 248.8 352 240S359.2'
    + ' 224 368 224h128C504.8 224 512 231.2 512 240S504.8 256 496 256zM496 192h'
    + '-128C359.2 192 352 184.8 352 176S359.2 160 368 160h128C504.8 160 512 167'
    + f'.2 512 176S504.8 192 496 192z"{icon_color}/></svg>&nbsp;&nbsp;&nbsp;'
    + 'Profiles'
)

suggestion_label_with_icon = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"'
    + f'{icon_dimensions}><path d="M256 32C114.6 32 .0272 125.1 .0272 240c0 49.'
    + '63 21.35 94.98 56.97 130.7c-12.5 50.37-54.27 95.27-54.77 95.77c-2.25 2.2'
    + '5-2.875 5.734-1.5 8.734C1.979 478.2 4.75 480 8 480c66.25 0 115.1-31.76 1'
    + '40.6-51.39C181.2 440.9 217.6 448 256 448c141.4 0 255.1-93.13 255.1-208S3'
    + f'97.4 32 256 32z"{icon_color}/></svg>&nbsp;&nbsp;&nbsp;Suggestions'
)

email_label_with_icon = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"'
    + f'{icon_dimensions}><path d="M464 64C490.5 64 512 85.49 512 112C512 127.1'
    + ' 504.9 141.3 492.8 150.4L275.2 313.6C263.8 322.1 248.2 322.1 236.8 313.6'
    + 'L19.2 150.4C7.113 141.3 0 127.1 0 112C0 85.49 21.49 64 48 64H464zM217.6 '
    + '339.2C240.4 356.3 271.6 356.3 294.4 339.2L512 176V384C512 419.3 483.3 44'
    + f'8 448 448H64C28.65 448 0 419.3 0 384V176L217.6 339.2z"{icon_color}/></s'
    + 'vg>&nbsp;&nbsp;&nbsp;Emails'
)

block_label_with_icon = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" '
    + f' {icon_dimensions}><path d="M256 417.1c-16.38 0-32.88-4.1-46.88-1'
    + '5.12L0 250.9v213.1C0 490.5 21.5 512 48 512h416c26.5 0 48-21.5 48-47.1V25'
    + '0.9l-209.1 151.1C288.9 412 272.4 417.1 256 417.1zM493.6 163C484.8 156 47'
    + '6.4 149.5 464 140.1v-44.12c0-26.5-21.5-48-48-48l-77.5 .0016c-3.125-2.25-'
    + '5.875-4.25-9.125-6.5C312.6 29.13 279.3-.3732 256 .0018C232.8-.3732 199.4'
    + ' 29.13 182.6 41.5c-3.25 2.25-6 4.25-9.125 6.5L96 48c-26.5 0-48 21.5-48 4'
    + '8v44.12C35.63 149.5 27.25 156 18.38 163C6.75 172 0 186 0 200.8v10.62l96 '
    + '69.37V96h320v184.7l96-69.37V200.8C512 186 505.3 172 493.6 163zM176 255.1'
    + 'h160c8.836 0 16-7.164 16-15.1c0-8.838-7.164-16-16-16h-160c-8.836 0-16 7.'
    + '162-16 16C160 248.8 167.2 255.1 176 255.1zM176 191.1h160c8.836 0 16-7.16'
    + '4 16-16c0-8.838-7.164-15.1-16-15.1h-160c-8.836 0-16 7.162-16 15.1C160 18'
    + f'4.8 167.2 191.1 176 191.1z"{icon_color}/></svg>&nbsp;&nbsp;&nbsp;Blocks'
)

log_label_with_icon = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"'
    + f' {icon_dimensions}><path d="M256 0C397.4 0 512 114.6 512 256C512 397.4 '
    + '397.4 512 256 512C201.7 512 151.2 495 109.7 466.1C95.2 455.1 91.64 436 1'
    + '01.8 421.5C111.9 407 131.8 403.5 146.3 413.6C177.4 435.3 215.2 448 256 4'
    + '48C362 448 448 362 448 256C448 149.1 362 64 256 64C202.1 64 155 85.46 12'
    + '0.2 120.2L151 151C166.1 166.1 155.4 192 134.1 192H24C10.75 192 0 181.3 0'
    + ' 168V57.94C0 36.56 25.85 25.85 40.97 40.97L74.98 74.98C121.3 28.69 185.3'
    + ' 0 255.1 0L256 0zM256 128C269.3 128 280 138.7 280 152V246.1L344.1 311C35'
    + '4.3 320.4 354.3 335.6 344.1 344.1C335.6 354.3 320.4 354.3 311 344.1L239 '
    + '272.1C234.5 268.5 232 262.4 232 256V152C232 138.7 242.7 128 256 128V128z'
    + f'"{icon_color}/></svg>&nbsp;&nbsp;&nbsp;Logs'
)

JET_SIDE_MENU_ITEMS = [
    {
        'label': ('People'),
        'app_label': 'Users',
        'items': [
            {'name': 'user', 'label': format_html(user_label_with_icon)},
            {'name': 'profile', 'label': format_html(profile_label_with_icon)},
        ],
    },
    {
        'label': ('Email'),
        'app_label': 'Emails',
        'items': [
            {
                'name': 'suggestion',
                'label': format_html(suggestion_label_with_icon),
            },
            {'name': 'email', 'label': format_html(email_label_with_icon)},
            {'name': 'block', 'label': format_html(block_label_with_icon)},
        ],
    },
    {
        'label': ('Adminitsration'),
        'app_label': 'admin',
        'items': [
            {'name': 'logentry', 'label': format_html(log_label_with_icon)}
        ],
    },
]
