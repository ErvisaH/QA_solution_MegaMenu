# QA_solution_megamenu

QA Strategy to verify the Mega Menu:

To implement the strategy, I used only Python because I found this version of implementation faster. The checks I am doing in this implementations are:

1- Check if link is broken

2- Check if the link is placed correctly

3- Check the images that are part of the Mega Menu if they are showing

To check if the link is broken, I use the function check_broken_link(link), which gets the href attribute, sends a request and when getting the status back, it checks if it is higher than 400. In that case it stores the broken link in a list which I can reference later.

Now for the second check, my strategy is to search for the text (or a piece of it) in the href attribute because there is no other way for me to know those links are correct since I am not yet part of the team (In my current company I have a list of href + respective title so I just check that whenever there are big changes, or changes that directly affect those parts). The function check_mega_menu_links(source) does that, takes the text and searches for it in the href. There are exceptions of course and I handled them by implementing a key-value dictionary in Python and search for alternatives instead.

The last check is for images, for which I use the check_mega_menu_imgs(source) which checks for the image for a source, and calls the check_broken_link(link) method to check if the source is broken.
