# Bakajohn 
## Links:
- [Official Website](https://timkuo25.github.io/bakajohn/)
- [Instagram](https://www.instagram.com/bakajohn8917/)
- [Twitter](https://twitter.com/johnbaka19)
- [Discord](https://discord.gg/Ck69thuxtx)

## Intro
### About John
Once upon a time, there was a guy named John. John is a lovely person who likes to play the guitar. John has a beautiful girlfriend, Jenny. Every 14th of every month, John always created a song for Jenny. Like every boy falling in love, he can do anything for his lover just to see her smile.

However, things were not going well all the time. Jenny was attracted to another guy, "Bagajong" from Taiwan. Jenny was obsessed with Bagajong's tattoo and his fierce appearance. In the end, Jenny cuckolded John and started a relationship with Bagajong.

After losing the love of his life, John lost his mind entirely. He became angry day by day. Finally, he becomes Bakajohn

### Dynamic NFT Introduction 
Every Bakajohn is a free mint dynamic NFT collectible. After each transaction, our picture will change its characteristics. It's a nice guy at first, but it will become more and more angry.

- step 1 - Normal
- step 2 - Hair + Facial expression
- step 3 - Clothes + Accessories

### Contract Mechanism
As every NFT does, every Bakajohn Token has its own metadata which stored in IPFS (InterPlanetary File System). After safeMinting, the token will be generated and point to its first stage URI using `setTokenURI()`.

Moreover, there is a struct `token` recording its own stage and trasaction time. Whenever the `_transfer()` function is called, the code are able to check the `token.stage` and trigger `evolveStage()`, which contains a function `_engenderURI()` inside. Combine all the things above, John would be able to become a TRUE BAKAJOHN really soon.
