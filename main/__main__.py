
from browser import Browser
from group import Group
def main():
    browser = Browser()
    browser.navigate(
    url='https://www.facebook.com',
    wait_for='facebook',
    error='Unable to load the Facebook website'
    )
    browser.enter_login_details(email='giantscrusher@gmail.com', password='whiteHole=x=2x=3x=4x')
    groupId = '150322621832912'
    #browser.joinGroup('150322621832912')
    group = Group(groupId)
    browser.getPostsv2(group)
    print(group.__repr__())
    group.toXml()
    group.toDb()
if __name__ == '__main__':
    main()
