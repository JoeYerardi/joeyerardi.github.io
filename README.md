# Joe Yerardi’s journalism portfolio

A static portfolio built with the Python standard library and published through GitHub Pages. Squarespace Domains manages the DNS for `joeyerardi.com`.

## Preview and edit

```sh
python3 build.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory public
```

Open [the local preview](http://127.0.0.1:8765/). Rerun the build after editing content.

- `content/recent.json` contains selected Philadelphia Inquirer stories in display order. The homepage shows the first three. The Work page shows the full list.
- `content/archive.json` contains the clips, original reporting notes and links migrated from Squarespace. Paragraphs can contain HTML links.
- `content/about.html` contains the biography and résumé.
- `build.py` defines the shared layout, homepage and Contact page. Styles live in `assets/`.

## Publish

1. Publish the source to [JoeYerardi/joeyerardi.github.io](https://github.com/JoeYerardi/joeyerardi.github.io) on GitHub. A public repository supports Pages on GitHub Free.
2. In repository settings, open **Pages** and select **GitHub Actions** as the source. Run the **Deploy portfolio to GitHub Pages** workflow if it has yet to run successfully.
3. Open [the GitHub Pages URL](https://joeyerardi.github.io/) and check the homepage, `/featured-work`, `/about`, and `/contact`. Each legacy route resolves to its trailing-slash equivalent. Subsequent pushes to `main` deploy automatically.

## Switch the domain

1. In GitHub’s account-level Pages settings, add `joeyerardi.com` and verify it using the TXT record GitHub gives you. Add that record in the Squarespace Domains DNS panel and keep it after verification.
2. In the repository’s **Settings → Pages**, set the custom domain to `joeyerardi.com`.
3. Save a copy of the current Squarespace DNS settings for rollback. Replace the Squarespace website records for the apex and `www` with the following records. Keep any existing email and unrelated verification records. Check for conflicting `AAAA`, `ALIAS`, and `www` records.

   | Host | Type | Value |
   | --- | --- | --- |
   | `@` | A | `185.199.108.153` |
   | `@` | A | `185.199.109.153` |
   | `@` | A | `185.199.110.153` |
   | `@` | A | `185.199.111.153` |
   | `www` | CNAME | `joeyerardi.github.io` |

4. After GitHub reports the DNS check passed and provisions the certificate, enable **Enforce HTTPS**. Verify the apex, the `www` redirect, the three legacy URLs, and email delivery if the domain handles email.
5. Keep the Squarespace website subscription available until the new site is verified at the custom domain. If rollback is needed, restore the previous Squarespace website records from the saved copy. Keep the domain registration active if retiring the website subscription.

[GitHub Pages publishing setup](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) · [GitHub domain ownership verification](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages) · [GitHub custom domain settings](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) · [Squarespace DNS setup](https://support.squarespace.com/hc/en-us/articles/215744668-Point-a-Squarespace-domain-to-another-site)
