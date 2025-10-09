/*
ZONELOTS cliff notes

Adding posts:
1) Copy the post template file.
2) Write the post content in the file.
3) Add a new object to the "posts" array, containing the post's title (this can include HTML), filename (not including the ".html" extension), and tag list (optional). Sample:
	{
		"title": `{{ POST TITLE }}`,
		"filename": `{{ YYYY-MM-DD-post-title }}`,
		"tags": [`tag 1`, `tag 2`, `tag 3`],
	},

Safe characters to use in tags:
	letters (upper- or lowercase)
	numbers
	? / : @ - . _ ~ ! $ & ' ( ) * + , ; = (question mark, slash, colon, at sign, hyphen-minus, period, underscore, tilde, exclamation mark, dollar, ampersand, apostrophe, left parenthesis, right parenthesis, asterisk, plus, comma, semicolon, equals)
	spaces (will be replaced by hyphens in tag urls)

Adding messages:
Add a new item in the "messages" array, containing the message content (this can include HTML, but should be inline content only)
*/


/* =============
	SETTINGS
============= */

const latestPostsCutoff = 5; // number of blog posts displayed on home page
const messagesOn = false; // whether or not to show a random message in the header

// links listed in header (nav) and footer (contact)
const navLinks = [
{	"name": `nami's dev diary`,	"filename": `index`,	},
{	"name": `tags`,			"filename": `tags`,		},
{	"name": `archive`,		"filename": `archive`,	},
];
//const contactLinks = [
//{	"name": `Neocities`,	"url": `https://nomnomnami.com/`,	},
//{	"name": `Itch`,			"url": `https://example.com/`,	},
//{	"name": `email`,		"url": `contact@example.com`,	},
//];


/* ===============
	BLOG POSTS
=============== */

const posts = [
//new posts here
{
	"title": `moving my adult works off itch.io...`,
	"filename": `2025-07-28-moving-my-adult-works-off-itchio`,
	"tags": [`misc`],
},
{
	"title": `dev diary: return to ash, and studio life!`,
	"filename": `2025-06-04-dev-diary-return-to-ash-and-studio-life`,
	"tags": [`dev diary`],
},
{
	"title": `site anniversary!`,
	"filename": `2025-03-18-site-anniversary`,
	"tags": [`misc`],
},
{
	"title": `ren'py tip #12 - cuter history screen`,
	"filename": `2025-02-22-cuter-history-screen`,
	"tags": [`ren'py tips`, `Astra's Garden`],
},
{
	"title": `hello, 2025!`,
	"filename": `2025-01-01-hello-2025`,
	"tags": [`goals`],
},
{
	"title": `dev diary - web dev and goodbye to cohost`,
	"filename": `2024-09-16-dev-diary-web-dev-and-goodbye-to-cohost`,
	"tags": [`dev diary`],
},
{
	"title": `cohost`,
	"filename": `2024-09-09-cohost`,
	"tags": [`misc`],
},
{
	"title": `dev diary - a new cat boy is here`,
	"filename": `2024-09-02-dev-diary-a-new-cat-boy-is-here`,
	"tags": [`dev diary`, `Syrup 2`],
},
{
	"title": `dev diary - astrology, and more about lime`,
	"filename": `2024-08-19-dev-diary-astrology-and-more-about-lime`,
	"tags": [`dev diary`, `Syrup 2`],
},
{
	"title": `dev diary - memos and menus (syrup 2)`,
	"filename": `2024-08-12-dev-diary-memos-and-menus-syrup-2`,
	"tags": [`dev diary`, `Syrup 2`],
},
{
	"title": `dev diary - fixing syrup 2's request system`,
	"filename": `2024-07-29-dev-diary-fixing-syrup-2s-request-system`,
	"tags": [`dev diary`, `Syrup 2`],
},
{
	"title": `dev diary - surprise, it's a syrup 2 update`,
	"filename": `2024-07-22-dev-diary-surprise-syrup-2-update`,
	"tags": [`dev diary`, `Syrup 2`],
},
{
	"title": `2024 plans (mid-year update)`,
	"filename": `2024-07-04-2024-plans-mid-year-update`,
	"tags": [`goals`],
},
{
	"title": `what, u want my backstory??`,
	"filename": `2024-04-20-my-backstory`,
	"tags": [`misc`],
},
{
	"title": `let me tell you about neocities`,
	"filename": `2024-03-29-let-me-tell-you-about-neocities`,
	"tags": [`advice`],
},
{
	"title": `let me tell you about a game i love`,
	"filename": `2024-03-11-let-me-tell-you-about-a-game-i-love`,
	"tags": [`misc`],
},
	
{
	"title": `ren'py tip #11 - adding an ending checklist... using LISTS`,
	"filename": `2024-03-09-ending-checklist2`,
	"tags": [`ren'py tips`],
},
{
	"title": `ren'py tip #10 - add an ending checklist using persistent variables`,
	"filename": `2024-03-04-ending-checklist`,
	"tags": [`ren'py tips`],
},
{
	"title": `ren'py tip #9 - customizing save names`,
	"filename": `2024-03-03-customizing-save-names`,
	"tags": [`ren'py tips`],
},	
{
	"title": `ren'py tip #8 - adding sound effects to your menus`,
	"filename": `2024-03-02-add-sfx-to-menus`,
	"tags": [`ren'py tips`],
},
{
	"title": `ren'py tip #7 - pare down that quick menu`,
	"filename": `2024-03-02-pare-down-that-quick-menu`,
	"tags": [`ren'py tips`],
},
{
	"title": `ren'py tip #6 - make an enticing title screen with SnowBlossom()`,
	"filename": `2024-03-01-snowblossom`,
	"tags": [`ren'py tips`],
},
{
	"title": `ren'py tip #5 - keyboard shortcut cheat sheet`,
	"filename": `2024-03-01-keyboard-shortcuts`,
	"tags": [`ren'py tips`],
},
{
	"title": `ren'py tip #4 - animate stuff with simple transforms`,
	"filename": `2024-03-01-animate-with-simple-transforms`,
	"tags": [`ren'py tips`],
},
{
	"title": `ren'py tip #3 - excluding certain files from your build`,
	"filename": `2024-02-29-excluding-files`,
	"tags": [`ren'py tips`],
},
{
	"title": `ren'py tip #2 - fixing outlines with line_overlap_split`,
	"filename": `2024-02-29-fixing-outlines`,
	"tags": [`ren'py tips`],
},
{
	"title": `ren'py tip #1 - scripting character expressions the fast and easy way`,
	"filename": `2024-02-29-scripting-character-expressions`,
	"tags": [`ren'py tips`],
},
	
{
	"title": `dev diary - the plush campaign is going but...`,
	"filename": `2024-02-19-dev-diary-the-plush-campaign-is-going`,
	"tags": [`dev diary`, `Sex Advice Succubus`, `music`],
},
{
	"title": `dev diary - treat 8, part 2`,
	"filename": `2024-02-05-dev-diary-treat-8-part-2`,
	"tags": [`dev diary`, `Lonely Wolf Treat`],
},
{
	"title": `Trick Comes Home - new characters`,
	"filename": `2024-01-22-Trick-Comes-Home-new-characters`,
	"tags": [`Lonely Wolf Treat`],
},
{
	"title": `dev diary - treat+BET news`,
	"filename": `2024-01-15-dev-diary-treat-BET-news`,
	"tags": [`dev diary`, `Lonely Wolf Treat`, `BAD END THEATER`],
},
{	"title": `2024 plans`,
	"filename": `2024-01-01-2024-plans`,
	"tags": [`goals`],
},
{
	"title": `a hastily written guide to getting into disgaea`,
	"filename": `2023-12-25-a-hastily-written-guide-to-getting-into-disgaea`,
	"tags": [`misc`],
},
{
	"title": `dev diary - tumblr revival era`,
	"filename": `2023-12-11-dev-diary-tumblr-revival-era`,
	"tags": [`dev diary`],
},
{
	"title": `dev diary - convention report`,
	"filename": `2023-11-20-dev-diary-convention-report`,
	"tags": [`dev diary`, `misc`],
},
{
	"title": `dev diary - treat treat treat treat treat`,
	"filename": `2023-11-06-dev-diary-treat-treat-treat-treat-treat`,
	"tags": [`dev diary`, `Lonely Wolf Treat`],
},
{
	"title": `dev diary - music, but on itch`,
	"filename": `2023-10-23-dev-diary-music-but-on-itch`,
	"tags": [`dev diary`, `music`],
},
{
	"title": `Packed to the Gills - postmortem`,
	"filename": `2023-10-04-Packed-to-the-Gills-postmortem`,
	"tags": [`postmortem`],
},
{
	"title": `dev diary - synth v process`,
	"filename": `2023-09-19-dev-diary-synth-v-process`,
	"tags": [`dev diary`, `music`],
},
{
	"title": `dev diary - pdf party`,
	"filename": `2023-08-28-dev-diary-pdf-party`,
	"tags": [`dev diary`, `another piece of candy`, `Syrup 2`],
},
{
	"title": `dev diary - picross on ur phone`,
	"filename": `2023-08-07-dev-diary-picross-on-ur-phone`,
	"tags": [`dev diary`, `Charm Studies`],
},
{
	"title": `dev diary - many things in progress`,
	"filename": `2023-07-17-dev-diary-many-things-in-progress`,
	"tags": [`dev diary`],
},
{
	"title": `dev diary - quick lil progress update`,
	"filename": `2023-07-03-dev-diary-quick-lil-progress-update`,
	"tags": [`dev diary`],
},
{
	"title": `dev diary - summer planning`,
	"filename": `2023-06-19-dev-diary-summer-planning`,
	"tags": [`dev diary`, `another piece of candy`],
},
{
	"title": `Princess Poffin and the Spider Invasion - postmortem`,
	"filename": `2023-06-05-Princess-Poffin-and-the-Spider-Invasion-postmortem`,
	"tags": [`postmortem`, `Princess Poffin`],
},
{
	"title": `dev diary - poffin game`,
	"filename": `2023-05-29-dev-diary-poffin-game`,
	"tags": [`dev diary`, `Princess Poffin`],
},
{
	"title": `dev diary - oops this chapter is too long`,
	"filename": `2023-05-15-dev-diary-oops-this-chapter-is-too-long`,
	"tags": [`dev diary`, `Lonely Wolf Treat`],
},
{
	"title": `Rain on Their Parade - postmortem`,
	"filename": `2023-05-02-Rain-on-Their-Parade-postmortem`,
	"tags": [`postmortem`],
},
{
	"title": `dev diary - treat 8, part 1`,
	"filename": `2023-04-24-dev-diary-treat-8-part-1`,
	"tags": [`dev diary`, `Lonely Wolf Treat`],
},
{
	"title": `tips for game writers`,
	"filename": `2023-04-18-tips-for-game-writers`,
	"tags": [`advice`],
},
{
	"title": `dev diary - plans plans plans`,
	"filename": `2023-04-03-dev-diary-plans-plans-plans`,
	"tags": [`dev diary`],
},
{
	"title": `Charm Studies - postmortem`,
	"filename": `2023-03-28-Charm-Studies-postmortem`,
	"tags": [`postmortem`, `Charm Studies`],
},
{
	"title": `dev diary - picross in ren'py`,
	"filename": `2023-03-13-dev-diary-picross-in-ren'py`,
	"tags": [`dev diary`, `Charm Studies`],
},
{
	"title": `you should make a visual novel for nanoreno`,
	"filename": `2023-02-28-you-should-make-a-visual-novel-for-nanoreno`,
	"tags": [`advice`],
},
{
	"title": `dev diary - qmin's music player`,
	"filename": `2023-02-20-dev-diary-qmin's-music-player`,
	"tags": [`dev diary`, `Sex Advice Succubus`],
},
{
	"title": `Sex Advice Succubus - postmortem`,
	"filename": `2023-02-07-Sex-Advice-Succubus-postmortem`,
	"tags": [`postmortem`, `Sex Advice Succubus`],
},
{
	"title": `dev diary - strawberry jam`,
	"filename": `2023-02-06-dev-diary-strawberry-jam`,
	"tags": [`dev diary`, `Sex Advice Succubus`],
},
{
	"title": `Lonely Wolf Treat - alternate ending plans`,
	"filename": `2023-01-30-lonely-wolf-treat-alternate-ending-plans`,
	"tags": [`Lonely Wolf Treat`],
},
{
	"title": `dev diary - slow beginnings for treat 8`,
	"filename": `2023-01-23-dev-diary-slow-beginnings-for-treat-8`,
	"tags": [`dev diary`, `Lonely Wolf Treat`],
},
{
	"title": `DATE TREAT - postmortem`,
	"filename": `2023-01-16-DATE-TREAT-postmortem`,
	"tags": [`postmortem`, `Lonely Wolf Treat`],
},
{
	"title": `Greenfinger! postmortem`,
	"filename": `2023-01-09-Greenfinger-postmortem`,
	"tags": [`postmortem`],
},
{
	"title": `dev diary - syrup 2 event management`,
	"filename": `2023-01-02-dev-diary-syrup-2-event-management`,
	"tags": [`dev diary`, `Syrup 2`],
},
{
	"title": `2023 plans`,
	"filename": `2023-01-01-2023-plans`,
	"tags": [`goals`],
},
{
	"title": `dev diary - syrup 2 build progress`,
	"filename": `2022-12-20-dev-diary-syrup-2-build-progress`,
	"tags": [`dev diary`, `Syrup 2`],
},
{
	"title": `dev diary - survey pre-results, and other plans`,
	"filename": `2022-12-05-dev-diary-survey-pre-results-and-other-plans`,
	"tags": [`dev diary`],
},
{
	"title": `dev diary - animation and... books, maybe?`,
	"filename": `2022-11-21-dev-diary-animation-and-books-maybe`,
	"tags": [`dev diary`, `another piece of candy`],
},
{
	"title": `dev diary - scattered thoughts`,
	"filename": `2022-11-07-dev-diary-scattered-thoughts`,
	"tags": [`dev diary`, `misc`],
},
{
	"title": `dev diary - syrup 2 status update`,
	"filename": `2022-10-17-dev-diary-syrup-2-status-update`,
	"tags": [`dev diary`, `Syrup 2`],
},
{
	"title": `another piece of candy retrospective`,
	"filename": `2022-10-10-another-piece-of-candy-retrospective`,
	"tags": [`another piece of candy`],
},
{
	"title": `her tears were my light - postmortem`,
	"filename": `2022-09-26-her-tears-were-my-light-postmortem`,
	"tags": [`postmortem`, `her tears were my light`],
},
{
	"title": `dev diary - trailer process`,
	"filename": `2022-09-12-dev-diary-trailer-process`,
	"tags": [`dev diary`, `her tears were my light`],
},
{
	"title": `dev diary - htwml gamepad-friendly UI`,
	"filename": `2022-08-29-dev-diary-htwml-gamepad-friendly-ui`,
	"tags": [`dev diary`, `htwml`],
},
{
	"title": `dev diary - lazy summer vibes`,
	"filename": `2022-08-22-dev-diary-lazy-summer-vibes`,
	"tags": [`dev diary`, `advice`],
},
{
	"title": `dev diary - lazy summer vibes`,
	"filename": `2022-08-01-dev-diary-pdf-making-and-other-release-stuff`,
	"tags": [`dev diary`, `Lonely Wolf Treat`],
},
{
	"title": `dev diary - writing tools`,
	"filename": `2022-07-18-dev-diary-writing-tools`,
	"tags": [`dev diary`],
},
{
	"title": `2022 plans (mid-year update)`,
	"filename": `2022-07-15-2022-plans-mid-year-update`,
	"tags": [`goals`],
},
{
	"title": `dev diary - staying organized`,
	"filename": `2022-07-04-dev-diary-staying-organized`,
	"tags": [`dev diary`],
},
{
	"title": `dev diary - treat bug collection`,
	"filename": `2022-06-20-dev-diary-treat-bug-collection`,
	"tags": [`dev diary`, `Lonely Wolf Treat`],
},
{
	"title": `dev diary - treat progress and tidying up ren'py code`,
	"filename": `2022-06-06-dev-diary-treat-progress-and-tidying-up-renpy-code`,
	"tags": [`dev diary`, `Lonely Wolf Treat`, `BAD END THEATER`],
},
{
	"title": `dev diary - treat status update`,
	"filename": `2022-05-23-dev-diary-treat-status-update`,
	"tags": [`dev diary`, `Lonely Wolf Treat`],
},
{
	"title": `astra's garden - postmortem`,
	"filename": `2022-05-09-astras-garden-postmortem`,
	"tags": [`postmortem`, `Astra's Garden`],
},
{
	"title": `dev diary - astra's garden prerelease stuff`,
	"filename": `2022-05-02-dev-diary-astras-garden-prerelease-stuff`,
	"tags": [`dev diary`, `Astra's Garden`],
},
{
	"title": `2022 plans`,
	"filename": `2021-12-14-2022-plans`,
	"tags": [`goals`],
},
{
	"title": `2021 plans (updated)`,
	"filename": `2021-06-10-2021-plans-updated`,
	"tags": [`goals`],
},
{
	"title": `2021 plans`,
	"filename": `2021-01-01-2021-plans`,
	"tags": [`goals`],
},
{
	"title": `2020 plans (revised)`,
	"filename": `2020-07-23-2020-plans-revised`,
	"tags": [`goals`],
},
{
	"title": `2020 plans`,
	"filename": `2020-01-24-2020-plans`,
	"tags": [`goals`],
},	
];



/* =============
	MESSAGES
============= */

const messages = [
	//`test message 1`,
	//`test message b`,
	//`this message includes <em>inline <abbr>HTML</abbr></em>`,
	//`this message includes <a href="https://zombo.com/" rel="external">a link</a>`,
];



/* ======================
	PAGE CONSTRUCTION
====================== */

// get current filepath and the relative paths to the posts folder and the index folder
const path = location.pathname.split("/");
const inPost = path.at(-2) === `posts`;
const pathToPosts = inPost ? `./` : `./posts/`;
const pathToInfo = inPost ? `../` : `./`;

// take a post in posts array and return a formatted link to that post
function formatPostLink(post) {
	return `<li><time>${post.filename.slice(0, 10)}</time> <a href="${pathToPosts}${post.filename}.html">${post.title}</a></li>`;
}

// convert tag to HTML id/link hash
function formatTagHash(tag) {
	return `--${tag.replaceAll(/\s+/g, `-`)}`;
}

/* ------------------
	HEADER/FOOTER
------------------ */

// write in main-nav and footer content
document.getElementById(`header`).innerHTML = `
<nav id="main-nav"><ul class="flex-list">${navLinks.map(link => `<li><a href="${pathToInfo}${link.filename}.html">${link.name}</a></li>`).join(``)}</ul></nav>
${messagesOn && messages.length > 0
? `<div id="header-message">${messages[Math.floor(Math.random() * messages.length)]}</div>`
: ``}
`;
//document.getElementById(`contact-links`).innerHTML = contactLinks.map(link => `<li><a href="${link.url}" rel="external">${link.name}</a></li>`).join(``);

/* ----------
	LISTS
---------- */

// build list of latest X blog posts for the home page
const latestPosts = document.getElementById(`latest-posts`);
if (latestPosts) latestPosts.innerHTML = posts.slice(0, latestPostsCutoff).map(formatPostLink).join(``);

// build list of all blog posts for the main blog page
const allPosts = document.getElementById(`all-posts`);
if (allPosts) allPosts.innerHTML = posts.map(formatPostLink).join(``);

// build tag list and list posts by tag on tags page
const tagsList = document.getElementById(`tag-index`);
if (tagsList) {
	const postsByTag = {};

	// for each tag, make a set of indices of posts with that tag
	posts.forEach((post, i) => post.tags.forEach(tag => {
		postsByTag[tag] ??= new Set();
		postsByTag[tag].add(i);
	}));

	tagsList.innerHTML = Object.entries(postsByTag).map(([tag, postIndices]) => `
	<li id="${formatTagHash(tag)}">
		<details>
			<summary>${tag}</summary>
			<ol class="post-list" reversed>${[...postIndices].map(i => formatPostLink(posts[i])).join(``)}</ol>
		</details>
	</li>
	`).join(``);

	// if URL includes hash with tag name, open its post list
	if (location.hash.length > 0) {
		const selectedTag = document.getElementById(location.hash.slice(1));
		if (selectedTag) selectedTag.querySelector(`details`).open = true;
	}
}

/* --------------
	BLOG POST
-------------- */

if (inPost) {
	// get index of post matching path (cut off file extension so if webhost cuts off extension the script still works)
	const i = posts.findIndex(post => post.filename === path.at(-1).split(`.html`)[0]);

	const postDate = document.getElementById(`post-date`);
	const pathDate = posts[i].filename.substring(0, 10);
	postDate.dateTime = pathDate;
	postDate.innerHTML = new Date(pathDate).toLocaleDateString();

	if (posts[i].tags) document.getElementById(`post-tags`).innerHTML = posts[i].tags.map(tag => `<li><a href="${pathToInfo}tags.html#${formatTagHash(tag)}">${tag}</a></li>`).join(``);

	// link to previous and next posts (if this post is first/latest, link to index instead of previous/next post)
	let postNav = ``;

	postNav += `<li>${i < posts.length - 1
	? `<a href="${pathToPosts}${posts[i + 1].filename}.html" rel="prev">${posts[i + 1].title}</a>`
	: `<a href="${pathToInfo}index.html" rel="index">back to index</a>`}</li>`;
	postNav += `<li>${i > 0
	? `<a href="${pathToPosts}${posts[i - 1].filename}.html" rel="next">${posts[i - 1].title}</a>`
	: `<a href="${pathToInfo}index.html" rel="index">back to index</a>`}</li>`;

	document.getElementById(`post-nav`).innerHTML = `<ul>${postNav}</ul>`;
}
